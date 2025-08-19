-- Page 1 (NPK)
INSERT INTO ingredients (code, name, nitrogen_percent, phosphorus_percent, potassium_percent, sulfur_percent, is_available, page_id) VALUES
('TSP','Triple Super Phosphate',0.0,46.0,0.0,0.5,true,1) ON CONFLICT (code) DO NOTHING;
INSERT INTO ingredients (code, name, nitrogen_percent, phosphorus_percent, potassium_percent, sulfur_percent, is_available, page_id) VALUES
('SSP','Single Super Phosphate',0.0,20.0,0.0,14.0,true,1) ON CONFLICT (code) DO NOTHING;
INSERT INTO ingredients (code, name, nitrogen_percent, phosphorus_percent, potassium_percent, sulfur_percent, is_available, page_id) VALUES
('AS','Ammonium Sulfate',21.0,0.0,60.0,24.0,true,1) ON CONFLICT (code) DO NOTHING;
INSERT INTO ingredients (code, name, nitrogen_percent, phosphorus_percent, potassium_percent, sulfur_percent, is_available, page_id) VALUES
('S_elem','Elemental Sulfur',0.0,0.0,60.0,100.0,true,1) ON CONFLICT (code) DO NOTHING;
INSERT INTO ingredients (code, name, nitrogen_percent, phosphorus_percent, potassium_percent, sulfur_percent, is_available, page_id) VALUES
('DAP','Diammonium Phosphate',18.0,46.0,0.0,0.8,true,1) ON CONFLICT (code) DO NOTHING;
INSERT INTO ingredients (code, name, nitrogen_percent, phosphorus_percent, potassium_percent, sulfur_percent, is_available, page_id) VALUES
('MAP','Monoammonium Phosphate',12.0,61.0,0.0,0.0,true,1) ON CONFLICT (code) DO NOTHING;
INSERT INTO ingredients (code, name, nitrogen_percent, phosphorus_percent, potassium_percent, sulfur_percent, is_available, page_id) VALUES
('Uree','Urea',46.0,0.0,0.0,0.0,true,1) ON CONFLICT (code) DO NOTHING;
INSERT INTO ingredients (code, name, nitrogen_percent, phosphorus_percent, potassium_percent, sulfur_percent, is_available, page_id) VALUES
('SOP','Sulfate of Potash',0.0,0.0,50.0,18.0,true,1) ON CONFLICT (code) DO NOTHING;
INSERT INTO ingredients (code, name, nitrogen_percent, phosphorus_percent, potassium_percent, sulfur_percent, is_available, page_id) VALUES
('MOP','Muriate of Potash',0.0,0.0,60.0,0.0,true,1) ON CONFLICT (code) DO NOTHING;
INSERT INTO ingredients (code, name, nitrogen_percent, phosphorus_percent, potassium_percent, sulfur_percent, is_available, page_id) VALUES
('Ballast','Trace Elements Mix',0.0,0.0,0.0,0.0,true,1) ON CONFLICT (code) DO NOTHING;

-- Page 2 (NPK-S)
INSERT INTO ingredients (code, name, nitrogen_percent, phosphorus_percent, potassium_percent, sulfur_percent, is_available, page_id) VALUES
('TSP','Triple Super Phosphate',0.0,46.5,0.0,1.0,true,2) ON CONFLICT (code) DO NOTHING;
INSERT INTO ingredients (code, name, nitrogen_percent, phosphorus_percent, potassium_percent, sulfur_percent, is_available, page_id) VALUES
('SSP','Single Super Phosphate',0.0,18.0,0.0,14.0,true,2) ON CONFLICT (code) DO NOTHING;
INSERT INTO ingredients (code, name, nitrogen_percent, phosphorus_percent, potassium_percent, sulfur_percent, is_available, page_id) VALUES
('AS','Ammonium Sulfate',21.0,0.0,60.0,24.0,true,2) ON CONFLICT (code) DO NOTHING;
INSERT INTO ingredients (code, name, nitrogen_percent, phosphorus_percent, potassium_percent, sulfur_percent, is_available, page_id) VALUES
('S_elem','Elemental Sulfur',0.0,0.0,60.0,100.0,true,2) ON CONFLICT (code) DO NOTHING;
INSERT INTO ingredients (code, name, nitrogen_percent, phosphorus_percent, potassium_percent, sulfur_percent, is_available, page_id) VALUES
('DAP','Diammonium Phosphate',18.0,46.0,0.0,0.8,true,2) ON CONFLICT (code) DO NOTHING;
INSERT INTO ingredients (code, name, nitrogen_percent, phosphorus_percent, potassium_percent, sulfur_percent, is_available, page_id) VALUES
('MAP','Monoammonium Phosphate',11.0,52.0,0.0,0.8,true,2) ON CONFLICT (code) DO NOTHING;
INSERT INTO ingredients (code, name, nitrogen_percent, phosphorus_percent, potassium_percent, sulfur_percent, is_available, page_id) VALUES
('Uree','Urea',46.0,0.0,0.0,0.0,true,2) ON CONFLICT (code) DO NOTHING;
INSERT INTO ingredients (code, name, nitrogen_percent, phosphorus_percent, potassium_percent, sulfur_percent, is_available, page_id) VALUES
('SOP','Sulfate of Potash',0.0,0.0,50.0,18.0,true,2) ON CONFLICT (code) DO NOTHING;
INSERT INTO ingredients (code, name, nitrogen_percent, phosphorus_percent, potassium_percent, sulfur_percent, is_available, page_id) VALUES
('MOP','Muriate of Potash',0.0,0.0,60.0,0.0,true,2) ON CONFLICT (code) DO NOTHING;
INSERT INTO ingredients (code, name, nitrogen_percent, phosphorus_percent, potassium_percent, sulfur_percent, is_available, page_id) VALUES
('NPK-S','Azote Phosphore Potassium Soufre',0.0,0.0,60.0,0.0,true,2) ON CONFLICT (code) DO NOTHING;
INSERT INTO ingredients (code, name, nitrogen_percent, phosphorus_percent, potassium_percent, sulfur_percent, is_available, page_id) VALUES
('Ballast','Trace Elements Mix',0.0,0.0,0.0,0.0,true,2) ON CONFLICT (code) DO NOTHING;
