INSERT INTO "archive_finder_archivefinder" 
("created", "modified", "name", "geometry", "start_date", "end_date", "is_active", "status", "rules")
VALUES %s
RETURNING "archive_finder_archivefinder"."id";