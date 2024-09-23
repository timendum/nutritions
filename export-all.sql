SELECT
    p.*,
    kcal.unit_value AS kcal,
    grassi.unit_value AS grassi,
    carb.unit_value AS carboidrati,
    z.unit_value AS zuccheri,
    fibr.unit_value AS fibre,
    prot.unit_value AS proteine
--    frutta.unit_value as frutta_value,
--    frutta.ingredient_text as frutta_text,
--    frutta.orig as frutta_orig,
--    cacao.unit_value as cacao_value,
    --cacao.ingredient_text as cacao_text,
--    cacao.orig as cacao_orig,
--    COALESCE(cm.name, m.name) AS category
FROM products AS p
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
LEFT JOIN product_facts AS fibr
    ON
        fibr.fact_id = 4
        AND p.id = fibr.product_id
LEFT JOIN product_facts AS prot
    ON
        prot.fact_id = 5
        AND p.id = prot.product_id
-- LEFT JOIN product_ingredients AS frutta
--     ON
--         frutta.ingredients_id = 1
--         AND p.id = frutta.product_id
-- LEFT JOIN product_ingredients AS cacao
--     ON
--         cacao.ingredients_id = 2
--         AND p.id = cacao.product_id
-- WHERE
--     m.id IN (34046, 300000001011216)
--     AND kcal.unit_value IS NOT NULL
--     AND (cm.id IS NULL OR cm.id NOT IN (34913, 35237, 35117))
ORDER BY kcal.unit_value ASC
