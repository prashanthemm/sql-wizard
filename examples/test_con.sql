SELECT
  n.nspname AS schema,
  p.proname AS name,
  pg_get_functiondef(p.oid) AS definition
FROM
  pg_proc p
  JOIN pg_namespace n ON p.pronamespace = n.oid
WHERE
  p.prokind = 'p'  -- 'p' = procedure (vs 'f' = function)
  AND n.nspname = 'public';
