-- Создание базы данных и выделенного пользователя
CREATE DATABASE car_rental;

-- Подключаемся к базе данных
\c car_rental;

-- Создаем пользователя с ограниченными правами
CREATE USER admin WITH PASSWORD 'admin';

-- 1. Создание роли owner
CREATE ROLE owner WITH LOGIN PASSWORD 'owner_password';

-- 2. Назначение прав роли owner
-- Полный доступ к базе данных
GRANT ALL PRIVILEGES ON DATABASE car_rental TO owner;

-- Полный доступ к схеме public
GRANT ALL PRIVILEGES ON SCHEMA public TO owner;

-- Полные права на все таблицы
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO owner;

-- Полные права на все последовательности (SERIAL, IDENTITY)
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO owner;

-- Полные права на все функции
GRANT ALL PRIVILEGES ON ALL FUNCTIONS IN SCHEMA public TO owner;

-- Разрешить роли создавать базы данных
ALTER ROLE owner CREATEDB;

-- Разрешить роли создавать других пользователей
ALTER ROLE owner CREATEROLE;

-- Разрешить роли входить в систему (если это не указано)
ALTER ROLE owner LOGIN;

-- Установка привилегий для будущих объектов
ALTER DEFAULT PRIVILEGES IN SCHEMA public
GRANT ALL PRIVILEGES ON TABLES TO owner;
ALTER DEFAULT PRIVILEGES IN SCHEMA public
GRANT ALL PRIVILEGES ON SEQUENCES TO owner;
ALTER DEFAULT PRIVILEGES IN SCHEMA public
GRANT ALL PRIVILEGES ON FUNCTIONS TO owner;

-- 3. Ограничение, чтобы роль не стала суперпользователем
ALTER ROLE owner NOSUPERUSER;

-- 4. Установка роли по умолчанию для подключения к базе данных
ALTER DATABASE car_rental OWNER TO owner;


-- Создание таблиц
CREATE TABLE Customers (
    passport_number CHAR(10) PRIMARY KEY, -- Серия и номер паспорта РФ (10 символов)
    first_name VARCHAR(50) NOT NULL, -- Ограничение до 50 символов
    middle_name VARCHAR(50), -- Ограничение до 50 символов
    last_name VARCHAR(50) NOT NULL, -- Ограничение до 50 символов
    email VARCHAR(100) UNIQUE, -- Ограничение до 100 символов
    phone_number CHAR(11) -- Номер телефона в формате РФ (11 цифр)
);

CREATE TABLE Models (
    brand_name VARCHAR(50), -- Ограничение до 50 символов
    model_name VARCHAR(50), -- Ограничение до 50 символов
    engine_volume DECIMAL(3, 1) NOT NULL, -- Например, 2.5 литра
    horsepower INT NOT NULL, -- Мощность двигателя
    transmission VARCHAR(20) NOT NULL, -- Тип коробки передач
    rental_cost DECIMAL(10, 2) NOT NULL, -- Стоимость аренды за день
    PRIMARY KEY (brand_name, model_name)
);

CREATE TABLE Cars (
    vin_car CHAR(17) PRIMARY KEY, -- VIN номер (строго 17 символов)
    brand_name VARCHAR(50), -- Ограничение до 50 символов
    model_name VARCHAR(50), -- Ограничение до 50 символов
    registration_number VARCHAR(9) UNIQUE, -- Госномер РФ (8-9 символов)
    color VARCHAR(30), -- Ограничение до 30 символов
    car_status VARCHAR(20) DEFAULT 'available', -- Статус машины (available или unavailable)
    FOREIGN KEY (brand_name, model_name) REFERENCES Models (brand_name, model_name),
    CONSTRAINT chk_car_status CHECK (car_status IN ('available', 'unavailable'))
);

CREATE TABLE Bookings (
    booking_id SERIAL PRIMARY KEY, -- Уникальный ID бронирования
    passport_number CHAR(10), -- Серия и номер паспорта РФ (10 символов)
    vin_car CHAR(17), -- VIN номер (строго 17 символов)
    start_date DATE NOT NULL, -- Дата начала аренды
    end_date DATE NOT NULL, -- Дата окончания аренды
    cost DECIMAL(10, 2), -- Итоговая стоимость аренды
    booking_status VARCHAR(20) DEFAULT 'active', -- Статус бронирования (active или completed)
    FOREIGN KEY (passport_number) REFERENCES Customers (passport_number),
    FOREIGN KEY (vin_car) REFERENCES Cars (vin_car),
    CONSTRAINT chk_booking_status CHECK (booking_status IN ('active', 'completed'))
);

-- Создание индекса по текстовому полю (например, email в таблице Customers)
CREATE INDEX idx_customers_email ON Customers (email);

-- Создание триггера для автоматического подсчета стоимости бронирования
CREATE OR REPLACE FUNCTION calculate_booking_cost()
RETURNS TRIGGER AS $$
BEGIN
    NEW.cost = (SELECT rental_cost * (NEW.end_date - NEW.start_date) FROM Cars c
                JOIN Models m ON c.brand_name = m.brand_name AND c.model_name = m.model_name
                WHERE c.vin_car = NEW.vin_car);
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_calculate_booking_cost
BEFORE INSERT OR UPDATE ON Bookings
FOR EACH ROW
EXECUTE FUNCTION calculate_booking_cost();

-- Предоставление прав пользователю car_user
GRANT CONNECT ON DATABASE car_rental TO admin;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO admin;
GRANT EXECUTE ON ALL FUNCTIONS IN SCHEMA public TO admin;







-- Создание функций ======================================================================================================================
-- Таблица клиентов ===========================================================
-- 1. Просмотр всех клиентов
CREATE OR REPLACE FUNCTION get_all_customers()
RETURNS TABLE (
    passport_number CHAR(10),
    first_name VARCHAR(50),
    middle_name VARCHAR(50),
    last_name VARCHAR(50),
    email VARCHAR(100),
    phone_number CHAR(11)
) AS $$
BEGIN
    RETURN QUERY SELECT * FROM Customers;
END;
$$ LANGUAGE plpgsql;

-- 2. Найти клиента по паспорту или почте
CREATE OR REPLACE FUNCTION find_customer_by_passport_or_email(search_value TEXT)
RETURNS TABLE (
    passport_number CHAR(10),
    first_name VARCHAR(50),
    middle_name VARCHAR(50),
    last_name VARCHAR(50),
    email VARCHAR(100),
    phone_number CHAR(11)
) AS $$
BEGIN
    RETURN QUERY SELECT * FROM Customers
    WHERE passport_number = search_value OR email = search_value;
END;
$$ LANGUAGE plpgsql;

-- 3. Добавить клиента
CREATE OR REPLACE FUNCTION add_customer(
    p_passport_number CHAR(10),
    p_first_name VARCHAR(50),
    p_middle_name VARCHAR(50),
    p_last_name VARCHAR(50),
    p_email VARCHAR(100),
    p_phone_number CHAR(11)
)
RETURNS VOID AS $$
BEGIN
    INSERT INTO Customers (passport_number, first_name, middle_name, last_name, email, phone_number)
    VALUES (p_passport_number, p_first_name, p_middle_name, p_last_name, p_email, p_phone_number);
END;
$$ LANGUAGE plpgsql;

-- 4. Удалить клиента по паспорту или почте
CREATE OR REPLACE FUNCTION delete_customer_by_passport_or_email(search_value TEXT)
RETURNS VOID AS $$
BEGIN
    DELETE FROM Customers WHERE passport_number = search_value OR email = search_value;
END;
$$ LANGUAGE plpgsql;