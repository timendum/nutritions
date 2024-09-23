CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY,
    [name] TEXT,
    brand TEXT,
    short TEXT,
    [description] TEXT,
    slug TEXT,
    price INTEGER,
    code TEXT,
    source TXT NOT NULL
) WITHOUT ROWID;


CREATE TABLE IF NOT EXISTS menus (
    id INTEGER PRIMARY KEY,
    [name] TEXT NOT NULL UNIQUE,
    slug TEXT,
    parent_id INTEGER
) WITHOUT ROWID;

CREATE TABLE IF NOT EXISTS item_menu (
    pm_id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id INTEGER,
    menu_id TEXT NOT NULL,
    UNIQUE (product_id, menu_id),
    FOREIGN KEY (product_id)
        REFERENCES products (id)
        ON DELETE CASCADE
        ON UPDATE NO ACTION,
    FOREIGN KEY (menu_id)
        REFERENCES menus (id)
        ON DELETE CASCADE
        ON UPDATE NO ACTION
);

CREATE TABLE IF NOT EXISTS nutrition_facts (
    label TEXT NOT NULL PRIMARY KEY,
    id INTEGER,
    unit_text TEXT NOT NULL
);

INSERT OR IGNORE INTO nutrition_facts (id, label, unit_text)
VALUES
	(1, 'energia', 'Kcal'),
	(1, 'enegia', 'Kcal'),
	(1, 'valore energetico', 'Kcal'),
	(1, 'val. energetico', 'Kcal'),
	(1, 'contenuto energetico', 'Kcal'),
	(2, 'grassi', 'g'),
	(2, 'grassi totali', 'g'),
	(2, 'grassi¿4¿', 'g'),
	(20, 'acidi grassi saturi', 'g'),
	(20, 'saturi', 'g'),
	(20, 'grassi saturi', 'g'),
	(3, 'carboidrati', 'g'),
	(30, 'zuccheri', 'g'),
	(30, 'zuchheri', 'g'),
	(30, '¹ zuccheri', 'g'),
	(30, 'zuccheri⁽¹⁾', 'g'),
	(4, 'fibre', 'g'),
	(4, 'fibra', 'g'),
	(4, 'fibra alimentare', 'g'),
	(5, 'proteine', 'g'),
	(6, 'sale', 'g'),
    (-1, 'energia (kj)', ''),
    (-1, 'energia (kcal)', ''),
    (-1, 'grassi (g)', ''),
    (-1, 'acidi grassi insaturi', ''),
    (-1, 'acidi grassi polinsaturi', ''),
    (-1, 'acidi grassi monoinsaturi', ''),
    (-1, 'acidi grassi saturi (g)', ''),
    (-1, 'carboidrati (g)', ''),
    (-1, 'zuccheri (g)', ''),
    (-1, 'fibre (g)', ''),
    (-1, 'proteine (g)', ''),
    (-1, 'sale (g)', ''),
    (-1, 'calcio', ''),
    (-1, 'ferro', ''),
    (-1, 'fosforo', ''),
    (-1, 'vitamina c1', ''),
    (-1, 'vitamina e', ''),
    (-1, 'magnesio', ''),
    (-1, 'vitamina a', ''),
    (-1, 'vitamina b1', ''),
    (-1, 'vitamina b12', ''),
    (-1, 'vitamina b2', ''),
    (-1, 'vitamina b6', ''),
    (-1, 'vitamina d', ''),
    (-1, 'vitamina c', ''),
    (-1, 'biotina', ''),
    (-1, 'zinco', ''),
    (-1, 'niacina', ''),
    (-1, 'beta carotene', ''),
    (-1, 'riboflavina', ''),
    (-1, 'tiamina', ''),
    (-1, 'tiammina', ''),
    (-1, 'lattosio', ''),
    (-1, 'acido pantotenico', ''),
    (-1, 'acido folico', ''),
    (-1, 'polioli', 'g');

CREATE TABLE IF NOT EXISTS product_facts (
    fact_id INTEGER,
    product_id INTEGER,
    unit_value FLOAT,
    PRIMARY KEY (fact_id, product_id),
    FOREIGN KEY (product_id)
        REFERENCES products (id)
        ON DELETE CASCADE
        ON UPDATE NO ACTION,
    FOREIGN KEY (fact_id)
        REFERENCES nutrition_facts (id)
        ON DELETE CASCADE
        ON UPDATE NO ACTION
);


CREATE TABLE IF NOT EXISTS main_ingredients (
    label TEXT NOT NULL PRIMARY KEY,
    id INTEGER
);

INSERT OR IGNORE INTO main_ingredients (id, label)
VALUES
    (1, 'nocciole'),
    (1, 'nocciola'),
    (1, 'nocciole italiane'),
    (1, 'nocciole tostate'),
    (1, 'arachidi tostate'),
    (1, 'arachidi'),
    (1, 'pistacchio'),
    (1, 'pistacchi bio'),
    (1, 'cocco'),
    (1, 'anacardi'),
    (1, 'mandorle pelate e tostate'),
    (1, 'mandorle'),
    (1, 'semi di girasole alto oleico tostati'),
    (2, 'gianduia'),
    (2, 'cacao'),
    (2, 'cacao magro'),
    (2, 'latte condensato zuccherato'),
    (2, 'cacao magro in polvere');

CREATE TABLE IF NOT EXISTS product_ingredients (
    ingredients_id INTEGER,
    product_id INTEGER,
    unit_value FLOAT,
    ingredient_text TEXT,
    orig TEXT,
    PRIMARY KEY (ingredients_id, product_id),
    FOREIGN KEY (product_id)
        REFERENCES products (id)
        ON DELETE CASCADE
        ON UPDATE NO ACTION,
    FOREIGN KEY (ingredients_id)
        REFERENCES main_ingredients (id)
        ON DELETE CASCADE
        ON UPDATE NO ACTION
);
