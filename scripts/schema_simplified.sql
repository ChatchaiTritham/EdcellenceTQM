-- ============================================================================
-- ADLI-LeTCI TQM Framework - Simplified Database Schema
-- ============================================================================
-- Full schema: 138 tables (12 fact + 26 dimension + 8 bridge + 92 lookup)
-- This simplified schema: 20 core tables for demonstration
-- PostgreSQL 13+
-- ============================================================================

-- ============================================================================
-- FACT TABLES (Core metrics and assessments)
-- ============================================================================

-- Fact: Assessment scores for process items (ADLI)
CREATE TABLE fact_assessment_scores (
    assessment_id SERIAL PRIMARY KEY,
    item_id VARCHAR(10) NOT NULL,
    department_id INT NOT NULL,
    assessment_cycle_id INT NOT NULL,
    assessment_date DATE NOT NULL,

    -- ADLI dimension scores [0,1]
    approach_score DECIMAL(4,3) CHECK (approach_score BETWEEN 0 AND 1),
    deployment_score DECIMAL(4,3) CHECK (deployment_score BETWEEN 0 AND 1),
    learning_score DECIMAL(4,3) CHECK (learning_score BETWEEN 0 AND 1),
    integration_score DECIMAL(4,3) CHECK (integration_score BETWEEN 0 AND 1),

    -- Computed item score [0,100]
    item_score DECIMAL(5,2) CHECK (item_score BETWEEN 0 AND 100),

    -- Metadata
    assessor_id INT,
    evidence_count INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    UNIQUE(item_id, department_id, assessment_cycle_id)
);

-- Fact: Results metrics (LeTCI)
CREATE TABLE fact_results_metrics (
    result_id SERIAL PRIMARY KEY,
    item_id VARCHAR(10) NOT NULL,
    department_id INT NOT NULL,
    assessment_cycle_id INT NOT NULL,
    measurement_date DATE NOT NULL,

    -- LeTCI dimension scores [0,1]
    level_score DECIMAL(4,3) CHECK (level_score BETWEEN 0 AND 1),
    trend_score DECIMAL(4,3) CHECK (trend_score BETWEEN 0 AND 1),
    comparison_score DECIMAL(4,3) CHECK (comparison_score BETWEEN 0 AND 1),
    integration_score DECIMAL(4,3) CHECK (integration_score BETWEEN 0 AND 1),

    -- Computed results score [0,100]
    results_score DECIMAL(5,2) CHECK (results_score BETWEEN 0 AND 100),

    -- Raw metric value
    metric_value DECIMAL(12,4),
    metric_unit VARCHAR(50),

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    UNIQUE(item_id, department_id, assessment_cycle_id)
);

-- Fact: Category-level aggregates
CREATE TABLE fact_category_aggregates (
    aggregate_id SERIAL PRIMARY KEY,
    category_name VARCHAR(50) NOT NULL,
    department_id INT NOT NULL,
    assessment_cycle_id INT NOT NULL,

    category_score DECIMAL(5,2) CHECK (category_score BETWEEN 0 AND 100),
    item_count INT,
    total_point_value INT,

    computed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    UNIQUE(category_name, department_id, assessment_cycle_id)
);

-- Fact: Organizational scores
CREATE TABLE fact_organizational_scores (
    org_score_id SERIAL PRIMARY KEY,
    department_id INT NOT NULL,
    assessment_cycle_id INT NOT NULL,

    organizational_score DECIMAL(5,2) CHECK (organizational_score BETWEEN 0 AND 100),
    maturity_level INT CHECK (maturity_level BETWEEN 1 AND 5),

    -- Integration Health Index
    ihi_score DECIMAL(4,3) CHECK (ihi_score BETWEEN 0 AND 1),

    assessment_date DATE NOT NULL,
    computed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    UNIQUE(department_id, assessment_cycle_id)
);

-- Fact: Gap analysis and priorities
CREATE TABLE fact_gap_analysis (
    gap_id SERIAL PRIMARY KEY,
    item_id VARCHAR(10) NOT NULL,
    department_id INT NOT NULL,
    assessment_cycle_id INT NOT NULL,

    current_score DECIMAL(5,2),
    target_score DECIMAL(5,2) DEFAULT 100.0,
    gap_score DECIMAL(5,2), -- (target - current)

    point_value INT,
    deployment_urgency DECIMAL(4,3), -- [0,1]
    priority_score DECIMAL(10,2), -- Gap priority (Equation 6)

    priority_rank INT, -- 1 = highest priority

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================================
-- DIMENSION TABLES (Reference data)
-- ============================================================================

-- Dimension: Departments
CREATE TABLE dim_department (
    department_id SERIAL PRIMARY KEY,
    department_code VARCHAR(10) UNIQUE NOT NULL,
    department_name VARCHAR(200) NOT NULL,
    faculty_name VARCHAR(200),
    department_type VARCHAR(50), -- Academic, Administrative, Support
    student_count INT,
    staff_count INT,
    active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Dimension: Assessment cycles
CREATE TABLE dim_assessment_cycle (
    cycle_id SERIAL PRIMARY KEY,
    cycle_code VARCHAR(20) UNIQUE NOT NULL,
    academic_year VARCHAR(10),
    cycle_start_date DATE NOT NULL,
    cycle_end_date DATE NOT NULL,
    cycle_type VARCHAR(50), -- Annual, Quarterly, Ad-hoc
    status VARCHAR(20) DEFAULT 'Active' -- Active, Closed, Archived
);

-- Dimension: Assessment items
CREATE TABLE dim_assessment_item (
    item_id VARCHAR(10) PRIMARY KEY,
    item_number VARCHAR(10),
    category_name VARCHAR(50) NOT NULL,
    item_description TEXT,
    item_type VARCHAR(20), -- Process, Results
    point_value INT NOT NULL,
    framework_source VARCHAR(50), -- Baldrige, EdPEx, TQF, AUN-QA
    active BOOLEAN DEFAULT TRUE
);

-- Dimension: Time
CREATE TABLE dim_time (
    date_id SERIAL PRIMARY KEY,
    full_date DATE UNIQUE NOT NULL,
    year INT,
    quarter INT,
    month INT,
    month_name VARCHAR(20),
    week_of_year INT,
    day_of_year INT,
    is_weekend BOOLEAN,
    academic_year VARCHAR(10),
    academic_semester INT
);

-- Dimension: Assessors
CREATE TABLE dim_assessor (
    assessor_id SERIAL PRIMARY KEY,
    employee_id VARCHAR(20) UNIQUE,
    full_name VARCHAR(200) NOT NULL,
    position VARCHAR(100),
    department_id INT REFERENCES dim_department(department_id),
    assessor_role VARCHAR(50), -- Coordinator, Dean, VP, External
    certification_level VARCHAR(50),
    active BOOLEAN DEFAULT TRUE
);

-- ============================================================================
-- BRIDGE TABLES (Multi-framework mappings)
-- ============================================================================

-- Bridge: Framework item mappings
CREATE TABLE bridge_framework_items (
    bridge_id SERIAL PRIMARY KEY,
    baldrige_item VARCHAR(10),
    edpex_item VARCHAR(10),
    tqf_form VARCHAR(10),
    aunqa_criterion VARCHAR(10),
    mapping_type VARCHAR(50), -- Direct, Partial, Conceptual
    mapping_confidence DECIMAL(3,2) CHECK (mapping_confidence BETWEEN 0 AND 1),
    notes TEXT
);

-- ============================================================================
-- LOOKUP TABLES (Framework parameters)
-- ============================================================================

-- Lookup: Category weights (EdPEx/Baldrige)
CREATE TABLE lookup_category_weights (
    category_name VARCHAR(50) PRIMARY KEY,
    baldrige_weight DECIMAL(4,3),
    edpex_weight DECIMAL(4,3),
    description TEXT
);

INSERT INTO lookup_category_weights VALUES
('Leadership', 0.120, 0.120, 'Leadership systems, governance, ethics'),
('Strategy', 0.085, 0.085, 'Strategic planning and objective deployment'),
('Customers', 0.085, 0.085, 'Stakeholder engagement and satisfaction'),
('Measurement', 0.100, 0.100, 'Data, analysis, knowledge management'),
('Workforce', 0.100, 0.100, 'Staff development and engagement'),
('Operations', 0.150, 0.150, 'Curriculum delivery and processes'),
('Results', 0.360, 0.360, 'Performance outcomes and trends');

-- Lookup: ADLI dimension weights
CREATE TABLE lookup_adli_weights (
    dimension_name VARCHAR(20) PRIMARY KEY,
    default_weight DECIMAL(4,3),
    nist_weight DECIMAL(4,3),
    description TEXT
);

INSERT INTO lookup_adli_weights VALUES
('Approach', 0.30, 0.30, 'Appropriateness and effectiveness of methods'),
('Deployment', 0.30, 0.30, 'Extent of implementation across organization'),
('Learning', 0.20, 0.20, 'Refinement through cycles of evaluation'),
('Integration', 0.20, 0.20, 'Alignment with organizational needs');

-- Lookup: LeTCI dimension weights
CREATE TABLE lookup_letci_weights (
    dimension_name VARCHAR(20) PRIMARY KEY,
    default_weight DECIMAL(4,3),
    baldrige_weight DECIMAL(4,3),
    description TEXT
);

INSERT INTO lookup_letci_weights VALUES
('Level', 0.40, 0.40, 'Current performance level'),
('Trend', 0.25, 0.25, 'Rate and direction of improvement'),
('Comparison', 0.25, 0.25, 'Comparative performance vs. benchmarks'),
('Integration', 0.10, 0.10, 'Alignment across categories');

-- Lookup: Maturity levels
CREATE TABLE lookup_maturity_levels (
    level INT PRIMARY KEY,
    label VARCHAR(50),
    min_score DECIMAL(5,2),
    max_score DECIMAL(5,2),
    description TEXT,
    typical_characteristics TEXT
);

INSERT INTO lookup_maturity_levels VALUES
(1, 'Reactive', 0, 20, 'Activity-based, undocumented',
 'Processes begin in response to problems; no systematic approach'),
(2, 'Early Systematic', 21, 40, 'Initial process definitions',
 'Basic processes defined but limited deployment; early learning'),
(3, 'Aligned', 41, 60, 'Systematic processes across units',
 'Systematic processes deployed across most units; fact-based learning'),
(4, 'Integrated', 61, 85, 'Strategic alignment',
 'Well-deployed processes fully aligned with strategy; evidence of refinement'),
(5, 'Role Model', 86, 100, 'Benchmarked innovation',
 'Innovative practices sustained over cycles; sector-leading performance');

-- ============================================================================
-- INDEXES (Performance optimization)
-- ============================================================================

-- Fact tables
CREATE INDEX idx_assessment_dept_cycle ON fact_assessment_scores(department_id, assessment_cycle_id);
CREATE INDEX idx_assessment_item ON fact_assessment_scores(item_id);
CREATE INDEX idx_results_dept_cycle ON fact_results_metrics(department_id, assessment_cycle_id);
CREATE INDEX idx_category_dept_cycle ON fact_category_aggregates(department_id, assessment_cycle_id);

-- Dimension tables
CREATE INDEX idx_dept_code ON dim_department(department_code);
CREATE INDEX idx_dept_active ON dim_department(active) WHERE active = TRUE;
CREATE INDEX idx_cycle_dates ON dim_assessment_cycle(cycle_start_date, cycle_end_date);
CREATE INDEX idx_item_category ON dim_assessment_item(category_name);

-- ============================================================================
-- VIEWS (Common queries)
-- ============================================================================

-- View: Latest assessment scores by department
CREATE VIEW vw_latest_department_scores AS
SELECT
    d.department_code,
    d.department_name,
    o.organizational_score,
    o.maturity_level,
    m.label as maturity_label,
    o.ihi_score,
    c.cycle_code,
    o.assessment_date
FROM fact_organizational_scores o
JOIN dim_department d ON o.department_id = d.department_id
JOIN dim_assessment_cycle c ON o.assessment_cycle_id = c.cycle_id
JOIN lookup_maturity_levels m ON o.maturity_level = m.level
WHERE o.assessment_date = (
    SELECT MAX(assessment_date)
    FROM fact_organizational_scores
    WHERE department_id = o.department_id
);

-- View: Top improvement priorities
CREATE VIEW vw_top_priorities AS
SELECT
    g.item_id,
    i.item_description,
    i.category_name,
    d.department_name,
    g.current_score,
    g.gap_score,
    g.priority_score,
    g.priority_rank
FROM fact_gap_analysis g
JOIN dim_assessment_item i ON g.item_id = i.item_id
JOIN dim_department d ON g.department_id = d.department_id
WHERE g.priority_rank <= 10
ORDER BY g.department_id, g.priority_rank;

-- ============================================================================
-- COMMENTS (Documentation)
-- ============================================================================

COMMENT ON TABLE fact_assessment_scores IS 'ADLI process item assessments with dimensional scoring (Equation 1)';
COMMENT ON TABLE fact_results_metrics IS 'LeTCI results metrics with dimensional scoring (Equation 2)';
COMMENT ON TABLE fact_category_aggregates IS 'Category-level scores as point-value weighted means (Equation 3)';
COMMENT ON TABLE fact_organizational_scores IS 'Organizational scores and IHI metrics (Equations 4-5)';
COMMENT ON TABLE fact_gap_analysis IS 'Gap-based improvement prioritization (Equation 6)';

-- ============================================================================
-- END OF SIMPLIFIED SCHEMA
-- Full 138-table schema available in schema_full.sql
-- ============================================================================
