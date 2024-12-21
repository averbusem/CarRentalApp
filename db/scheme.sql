-- CREATE DATABASE car_rental;

ALTER DATABASE car_rental OWNER TO db_creator;

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
    cost DECIMAL(10, 2) DEFAULT 0.00, -- Итоговая стоимость аренды (будет вычисляться с помощью тригерра)
    booking_status VARCHAR(20) DEFAULT 'active', -- Статус бронирования (active или completed)
    FOREIGN KEY (passport_number) REFERENCES Customers (passport_number),
    FOREIGN KEY (vin_car) REFERENCES Cars (vin_car),
    CONSTRAINT chk_booking_status CHECK (booking_status IN ('active', 'completed'))
);

-- Создание индекса по текстовому полю (например, email в таблице Customers)
CREATE INDEX idx_customers_email ON Customers (email);




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
    WHERE Customers.passport_number = search_value OR Customers.email = search_value;
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

-- Таблица автопарк ===========================================================
-- 1. Просмотр всех машин
CREATE OR REPLACE FUNCTION get_all_cars()
RETURNS TABLE (
    vin_car CHAR(17),
    brand_name VARCHAR(50),
    model_name VARCHAR(50),
    rental_cost DECIMAL(10, 2), -- Стоимость аренды стоит после model_name!
    registration_number VARCHAR(9),
    color VARCHAR(30),
    car_status VARCHAR(20),
    engine_volume DECIMAL(3, 1),
    horsepower INT,
    transmission VARCHAR(20)
) AS $$
BEGIN
    RETURN QUERY SELECT
        c.vin_car,
        c.brand_name,
        c.model_name,
        m.rental_cost, -- Стоимость аренды стоит после model_name!
        c.registration_number,
        c.color,
        c.car_status,
        m.engine_volume,
        m.horsepower,
        m.transmission
    FROM Cars c JOIN Models m
    ON c.brand_name = m.brand_name AND c.model_name = m.model_name;
END;
$$ LANGUAGE plpgsql;


-- 2. Просмотр свободных машин
CREATE OR REPLACE FUNCTION get_all_available_cars()
RETURNS TABLE (
    vin_car CHAR(17),
    brand_name VARCHAR(50),
    model_name VARCHAR(50),
    rental_cost DECIMAL(10, 2), -- Стоимость аренды
    registration_number VARCHAR(9),
    color VARCHAR(30),
    car_status VARCHAR(20),
    engine_volume DECIMAL(3, 1),
    horsepower INT,
    transmission VARCHAR(20)
) AS $$
BEGIN
    RETURN QUERY SELECT
        c.vin_car,
        c.brand_name,
        c.model_name,
        m.rental_cost,
        c.registration_number,
        c.color,
        c.car_status,
        m.engine_volume,
        m.horsepower,
        m.transmission
    FROM Cars c JOIN Models m
    ON c.brand_name = m.brand_name AND c.model_name = m.model_name
    WHERE c.car_status = 'available';
END;
$$ LANGUAGE plpgsql;



--3. Найти авто
CREATE OR REPLACE FUNCTION find_cars(
    p_brand_name VARCHAR(50),
    p_model_name VARCHAR(50)
)
RETURNS TABLE (
    vin_car CHAR(17),
    brand_name VARCHAR(50),
    model_name VARCHAR(50),
    rental_cost DECIMAL(10, 2),
    registration_number VARCHAR(9),
    color VARCHAR(30),
    car_status VARCHAR(20),
    engine_volume DECIMAL(3, 1),
    horsepower INT,
    transmission VARCHAR(20)
) AS $$
BEGIN
    RETURN QUERY SELECT
        c.vin_car,
        c.brand_name,
        c.model_name,
        m.rental_cost,
        c.registration_number,
        c.color,
        c.car_status,
        m.engine_volume,
        m.horsepower,
        m.transmission
    FROM Cars c JOIN Models m
    ON c.brand_name = m.brand_name AND c.model_name = m.model_name
    WHERE c.brand_name = p_brand_name AND c.model_name = p_model_name;
END;
$$ LANGUAGE plpgsql;



--4. Добавить авто
CREATE OR REPLACE FUNCTION add_car(
    p_vin_car CHAR(17),
    p_registration_number VARCHAR(9),
    p_brand_name VARCHAR(50),
    p_model_name VARCHAR(50),
    p_color VARCHAR(30)
)
RETURNS VOID AS $$
BEGIN
    INSERT INTO Cars (vin_car, registration_number, brand_name, model_name, color, car_status)
    VALUES (p_vin_car, p_registration_number, p_brand_name, p_model_name, p_color, 'available');
END;
$$ LANGUAGE plpgsql;



--5. Удалить авто
CREATE OR REPLACE FUNCTION delete_car(p_vin_car CHAR(17))
RETURNS VOID AS $$
BEGIN
    DELETE FROM Cars
    WHERE vin_car = p_vin_car;
END;
$$ LANGUAGE plpgsql;


-- Таблица заказы ===========================================================
--1. Посмотреть все заказы
CREATE OR REPLACE FUNCTION get_all_bookings()
RETURNS TABLE (
    vin_car CHAR(17),
    passport_number CHAR(10),
    first_name VARCHAR(50),
    middle_name VARCHAR(50),
    cost DECIMAL(10, 2),
    booking_status VARCHAR(20),
    start_date DATE,
    end_date DATE
) AS $$
BEGIN
    RETURN QUERY SELECT
        b.vin_car,
        c.passport_number,
        c.first_name,
        c.middle_name,
        b.cost,
        b.booking_status,
        b.start_date,
        b.end_date
    FROM Customers c JOIN Bookings b
    ON c.passport_number = b.passport_number;
END;
$$ LANGUAGE plpgsql;


--2. Посмотреть действующие заказы
CREATE OR REPLACE FUNCTION get_active_bookings()
RETURNS TABLE (
    vin_car CHAR(17),
    passport_number CHAR(10),
    first_name VARCHAR(50),
    middle_name VARCHAR(50),
    cost DECIMAL(10, 2),
    booking_status VARCHAR(20),
    start_date DATE,
    end_date DATE
) AS $$
BEGIN
    RETURN QUERY SELECT
        b.vin_car,
        c.passport_number,
        c.first_name,
        c.middle_name,
        b.cost,
        b.booking_status,
        b.start_date,
        b.end_date
    FROM Customers c JOIN Bookings b
    ON c.passport_number = b.passport_number
    WHERE b.booking_status = 'active';
END;
$$ LANGUAGE plpgsql;


--3. Создать заказ
CREATE OR REPLACE FUNCTION create_booking(
    p_passport_number CHAR(10),
    p_vin_car CHAR(17),
    p_start_date DATE,
    p_end_date DATE
)
RETURNS VOID AS $$
BEGIN
    --(стоимость будет вычисляться триггером)
    INSERT INTO Bookings (passport_number, vin_car, start_date, end_date)
    VALUES (p_passport_number, p_vin_car, p_start_date, p_end_date);

    -- Обновляем статус автомобиля на 'unavailable'
    UPDATE Cars SET car_status = 'unavailable'
    WHERE vin_car = p_vin_car;
END;
$$ LANGUAGE plpgsql;


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


--4. Закрыть заказ
CREATE OR REPLACE FUNCTION close_booking(
    p_passport_number CHAR(10),
    p_vin_car CHAR(17)
)
RETURNS VOID AS $$
BEGIN
    -- Обновляем статус бронирования на 'completed'
    UPDATE Bookings SET booking_status = 'completed'
    WHERE passport_number = p_passport_number
      AND vin_car = p_vin_car
      AND booking_status = 'active'; -- Обновляем только активные бронирования

    -- Обновляем статус автомобиля на 'available'
    UPDATE Cars
    SET car_status = 'available'
    WHERE vin_car = p_vin_car
      AND car_status = 'unavailable'; -- Обновляем только те автомобили, которые в данный момент недоступны

END;
$$ LANGUAGE plpgsql;

-- Таблица модели ===========================================================
-- 1. Просмотр всех моделей
CREATE OR REPLACE FUNCTION get_all_models()
RETURNS TABLE (
    brand_name VARCHAR(50),
    model_name VARCHAR(50),
    engine_volume DECIMAL(3, 1),
    horsepower INT,
    transmission VARCHAR(20),
    rental_cost DECIMAL(10, 2)
) AS $$
BEGIN
    RETURN QUERY SELECT * FROM Models;
END;
$$ LANGUAGE plpgsql;

-- 2. Найти модель по марке и названию
CREATE OR REPLACE FUNCTION find_model_by_brand_and_name(
    p_brand_name VARCHAR(50),
    p_model_name VARCHAR(50)
)
RETURNS TABLE (
    brand_name VARCHAR(50),
    model_name VARCHAR(50),
    engine_volume DECIMAL(3, 1),
    horsepower INT,
    transmission VARCHAR(20),
    rental_cost DECIMAL(10, 2)
) AS $$
BEGIN
    RETURN QUERY SELECT * FROM Models
    WHERE brand_name = p_brand_name AND model_name = p_model_name;
END;
$$ LANGUAGE plpgsql;


-- 3. Добавить модель
CREATE OR REPLACE FUNCTION add_new_model(
    p_brand_name VARCHAR(50),
    p_model_name VARCHAR(50),
    p_engine_volume DECIMAL(3, 1),
    p_horsepower INT,
    p_transmission VARCHAR(20),
    p_rental_cost DECIMAL(10, 2)
)
RETURNS VOID AS $$
BEGIN
    INSERT INTO Models (brand_name, model_name, engine_volume, horsepower, transmission, rental_cost)
    VALUES (p_brand_name, p_model_name, p_engine_volume, p_horsepower, p_transmission, p_rental_cost);
END;
$$ LANGUAGE plpgsql;


-- 4. Удалить модель по марке и названию
CREATE OR REPLACE FUNCTION delete_model(
    p_brand_name VARCHAR(50),
    p_model_name VARCHAR(50)
)
RETURNS VOID AS $$
BEGIN
    DELETE FROM Models
    WHERE brand_name = p_brand_name AND model_name = p_model_name;
END;
$$ LANGUAGE plpgsql;

-- 5. Изменить стоимость аренды модели
CREATE OR REPLACE FUNCTION update_rental_cost(
    p_brand_name VARCHAR(50),
    p_model_name VARCHAR(50),
    p_new_rental_cost DECIMAL(10, 2)
)
RETURNS VOID AS $$
BEGIN
    UPDATE Models
    SET rental_cost = p_new_rental_cost
    WHERE brand_name = p_brand_name AND model_name = p_model_name;
END;
$$ LANGUAGE plpgsql;



-- Очистка базы данных ===========================================================
--1. Очистить все таблицы
CREATE OR REPLACE FUNCTION clear_all_tables()
RETURNS VOID AS $$
BEGIN
    -- Очищаем таблицы в порядке их зависимости
    TRUNCATE TABLE Bookings CASCADE;
    TRUNCATE TABLE Cars CASCADE;
    TRUNCATE TABLE Models CASCADE;
    TRUNCATE TABLE Customers CASCADE;
END;
$$ LANGUAGE plpgsql;

--2. Очистить таблицу cars
CREATE OR REPLACE FUNCTION clear_cars_table()
RETURNS VOID AS $$
BEGIN
    -- Удаляем автомобили, для которых нет активных бронирований
    DELETE FROM Cars
    WHERE vin_car NOT IN (
        SELECT vin_car
        FROM Bookings
        WHERE booking_status = 'active'
    );
END;
$$ LANGUAGE plpgsql;

--3. Очистить таблицу customers
CREATE OR REPLACE FUNCTION clear_customers_table()
RETURNS VOID AS $$
BEGIN
    -- Удаляем клиентов, у которых нет активных бронирований
    DELETE FROM Customers
    WHERE passport_number NOT IN (
        SELECT passport_number
        FROM Bookings
        WHERE booking_status = 'active'
    );
END;
$$ LANGUAGE plpgsql;

--4. Очистить таблицу Bookings
CREATE OR REPLACE FUNCTION clear_bookings_table()
RETURNS VOID AS $$
BEGIN
    -- Удаляем завершённые заказы
    DELETE FROM Bookings
    WHERE booking_status = 'completed';
END;
$$ LANGUAGE plpgsql;



-- Проверяем, существует ли роль "owner"
DO $$
BEGIN
    IF NOT EXISTS (SELECT FROM pg_roles WHERE rolname = 'owner') THEN
        -- Создаем роль "owner", если она еще не существует
        CREATE ROLE owner WITH PASSWORD 'owner' LOGIN CREATEDB CREATEROLE NOSUPERUSER;
        RAISE NOTICE 'Роль "owner" успешно создана.';
    ELSE
        RAISE NOTICE 'Роль "owner" уже существует.';
    END IF;
END
$$;

-- Назначение прав роли "owner"
GRANT ALL PRIVILEGES ON DATABASE car_rental TO owner;
GRANT ALL PRIVILEGES ON SCHEMA public TO owner;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO owner;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO owner;
GRANT ALL PRIVILEGES ON ALL FUNCTIONS IN SCHEMA public TO owner;
-- Установка привилегий для будущих объектов
ALTER DEFAULT PRIVILEGES IN SCHEMA public
GRANT ALL PRIVILEGES ON TABLES TO owner;
ALTER DEFAULT PRIVILEGES IN SCHEMA public
GRANT ALL PRIVILEGES ON SEQUENCES TO owner;
ALTER DEFAULT PRIVILEGES IN SCHEMA public
GRANT ALL PRIVILEGES ON FUNCTIONS TO owner;


-- Проверяем, существует ли роль "admin"
DO $$
BEGIN
    IF NOT EXISTS (SELECT FROM pg_roles WHERE rolname = 'admin') THEN
        -- Создаем роль "admin", если она еще не существует
        CREATE USER admin WITH PASSWORD 'admin';
        RAISE NOTICE 'Роль "admin" успешно создана.';
    ELSE
        RAISE NOTICE 'Роль "admin" уже существует.';
    END IF;
END
$$;

-- Предоставление прав пользователю car_user
GRANT CONNECT ON DATABASE car_rental TO admin;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO admin;
GRANT EXECUTE ON ALL FUNCTIONS IN SCHEMA public TO admin;
GRANT USAGE, SELECT ON SEQUENCE bookings_booking_id_seq TO admin;