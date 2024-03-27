SELECT
    p.*,
    kcal.unit_value AS kcal,
    grassi.unit_value AS grassi,
    carb.unit_value AS carboidrati,
    z.unit_value AS zuccheri,
    prot.unit_value AS proteine,
    COALESCE(cm.name, m.name) AS category
FROM menus AS m
LEFT JOIN menus AS cm
    ON
        m.id = cm.parent_id
LEFT JOIN products AS p
INNER JOIN item_menu AS im
    ON
        p.id = im.product_id
        AND im.menu_id IN (m.id, cm.id)
LEFT JOIN product_facts AS kcal
    ON
        kcal.fact_id = 1
        AND p.id = kcal.product_id
LEFT JOIN product_facts AS grassi
    ON
        grassi.fact_id = 2
        AND p.id = grassi.product_id
LEFT JOIN product_facts AS carb
    ON
        carb.fact_id = 3
        AND p.id = carb.product_id
LEFT JOIN product_facts AS z
    ON
        z.fact_id = 30
        AND p.id = z.product_id
LEFT JOIN product_facts AS prot
    ON
        prot.fact_id = 5
        AND p.id = prot.product_id
WHERE
    m.id IN (34045, 300000001011217)
    AND kcal.unit_value IS NOT NULL
    AND (cm.id IS NULL OR cm.id NOT IN (34913, 35237, 35117))
ORDER BY kcal.unit_value ASC
