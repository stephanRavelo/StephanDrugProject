-- question 1
SELECT
    t.date AS date,
    SUM(t.prod_price) AS ventes
FROM transactions t
WHERE CONVERT(DATETIME,t.date ,103)>=CONVERT(DATETIME,"01/01/2019" ,103)
      AND  CONVERT(DATETIME,t.date ,103) < CONVERT(DATETIME,"01/01/2020" ,103)
GROUP BY date
ORDER BY t.date asc

-- question 2
SELECT  t.clientid,
        vm.vente_m AS vente_meuble,
        vd.vente_d AS vente_deco
FROM transactions t
LEFT JOIN
    (
        SELECT  tr.date,
                sum(tr.prod_price) AS vente_m,
                tr.clientid
        FROM transactions tr
        LEFT JOIN product_nomenclature pn ON tr.prop_id = pn.product_id
        WHERE pn.product_type="MEUBLE" AND (CONVERT(DATETIME,tr.date ,103)>=CONVERT(DATETIME,"01/01/2019" ,103)
                                            AND  CONVERT(DATETIME,tr.date ,103) < CONVERT(DATETIME,"01/01/2020" ,103)
                                            )
        GROUP BY tr.clientid, tr.date
    ) as vm
LEFT JOIN
    (
        SELECT  tra.date,
                sum(tra.prod_price) AS vente_m,
                tra.clientid
        FROM transactions tra
        LEFT JOIN product_nomenclature pno ON tra.prop_id = pno.product_id
        WHERE pno.product_type="DECO" AND (CONVERT(DATETIME,tra.date ,103)>=CONVERT(DATETIME,"01/01/2019" ,103)
                                            AND  CONVERT(DATETIME,tra.date ,103) < CONVERT(DATETIME,"01/01/2020" ,103)
                                            )
        GROUP BY tra.clientid, tra.date
    ) as vd
---