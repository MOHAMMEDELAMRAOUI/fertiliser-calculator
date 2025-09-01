CREATE TABLE IF NOT EXISTS ingredients (
    id SERIAL PRIMARY KEY,
    code TEXT NOT NULL UNIQUE,
    name TEXT NOT NULL,
    nitrogen_percent NUMERIC NOT NULL,
    phosphorus_percent NUMERIC NOT NULL,
    potassium_percent NUMERIC NOT NULL,
    sulfur_percent NUMERIC NOT NULL,
    is_available BOOLEAN NOT NULL DEFAULT true,
    page_id INT NOT NULL DEFAULT 1,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);


INSERT INTO ingredients (code, name, nitrogen_percent, phosphorus_percent, potassium_percent, sulfur_percent, is_available, page_id)
VALUES
('TSP', 'Triple Super Phosphate', 0.0, 46.0, 0.0, 0.5, true, 1),
('SSP', 'Single Super Phosphate', 0.0, 20.0, 0.0, 14.0, true, 1),
('AS', 'Ammonium Sulfate', 21.0, 0.0, 0.0, 24.0, true, 1),
('S_elem', 'Elemental Sulfur', 0.0, 0.0, 0.0, 100.0, true, 1),
('DAP', 'Diammonium Phosphate', 18.0, 46.0, 0.0, 0.8, true, 1),
('MAP', 'Monoammonium Phosphate', 12.0, 52.0, 0.0, 0.8, true, 1),
('Uree', 'Urea', 46.0, 0.0, 0.0, 0.0, true, 1),
('SOP', 'Sulfate of Potash', 0.0, 0.0, 50.0, 18.0, true, 1),
('MOP', 'Muriate of Potash', 0.0, 0.0, 60.0, 0.0, true, 1),
('Ballast', 'Trace Elements Mix', 0.0, 0.0, 0.0, 0.0, true, 1),

('TSP1', 'Triple Super Phosphate', 0.0, 46.5, 0.0, 1.0, true, 2),
('SSP1', 'Single Super Phosphate', 0.0, 18.0, 0.0, 14.0, true, 2),
('AS1', 'Ammonium Sulfate', 21.0, 0.0, 0.0, 24.0, true, 2),
('S_elem1', 'Elemental Sulfur', 0.0, 0.0, 0.0, 100.0, true, 2),
('DAP1', 'Diammonium Phosphate', 18.0, 46.0, 0.0, 0.8, true, 2),
('MAP1', 'Monoammonium Phosphate', 11.0, 52.0, 0.0, 0.8, true, 2),
('Uree1', 'Urea', 46.0, 0.0, 0.0, 0.0, true, 2),
('SOP1', 'Sulfate of Potash', 0.0, 0.0, 50.0, 18.0, true, 2),
('MOP1', 'Muriate of Potash', 0.0, 0.0, 60.0, 0.0, true, 2),
('NPK-S1', 'Azote Phosphore Potassium Soufre', 0.0, 0.0, 0.0, 0.0, true, 2),
('Ballast1', 'Trace Elements Mix', 0.0, 0.0, 0.0, 0.0, true, 2);
