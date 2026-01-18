@echo off
echo =========================
echo Installing TBP database
echo =========================

REM === PostgreSQL path (prilagoditi ako je potrebno) ===
set PSQL="C:\Program Files\PostgreSQL\18\bin\psql.exe"

REM 
set DB_NAME=tbp_nvugrinec22
set DB_USER=postgres

echo Creating database...
%PSQL% -U %DB_USER% -f database\install\01_create_database.sql

echo Creating types and domains...
%PSQL% -U %DB_USER% -d %DB_NAME% -f database\install\02_types_domains.sql

echo Creating tables...
%PSQL% -U %DB_USER% -d %DB_NAME% -f database\install\03_tables.sql

echo Creating triggers...
%PSQL% -U %DB_USER% -d %DB_NAME% -f database\install\04_triggers.sql

echo Creating views...
%PSQL% -U %DB_USER% -d %DB_NAME% -f database\install\05_views.sql

echo Creating rules...
%PSQL% -U %DB_USER% -d %DB_NAME% -f database\install\06_rules.sql



echo =========================
echo Database installed successfully
echo =========================
pause
