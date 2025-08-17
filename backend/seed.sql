INSERT INTO ingredients (code, name, nitrogen_percent, phosphorus_percent, potassium_percent, sulfur_percent, is_available)
VALUES
('UREE','Urée',46,0,0,0, true)
ON CONFLICT (code) DO NOTHING;

INSERT INTO ingredients (code, name, nitrogen_percent, phosphorus_percent, potassium_percent, sulfur_percent, is_available)
VALUES
('DAP','Diammonium Phosphate',18,46,0,0,true)
ON CONFLICT (code) DO NOTHING;

INSERT INTO ingredients (code, name, nitrogen_percent, phosphorus_percent, potassium_percent, sulfur_percent, is_available)
VALUES
('MAP','Monoammonium Phosphate',11,52,0,0,true)
ON CONFLICT (code) DO NOTHING;

INSERT INTO ingredients (code, name, nitrogen_percent, phosphorus_percent, potassium_percent, sulfur_percent, is_available)
VALUES
('MOP','Muriate of Potash (KCl)',0,0,60,0,true)
ON CONFLICT (code) DO NOTHING;

INSERT INTO ingredients (code, name, nitrogen_percent, phosphorus_percent, potassium_percent, sulfur_percent, is_available)
VALUES
('AS','Ammonium Sulfate',21,0,0,24,true)
ON CONFLICT (code) DO NOTHING;