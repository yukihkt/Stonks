DROP DATABASE IF EXISTS `stonks`;
CREATE DATABASE IF NOT EXISTS `stonks` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci;
USE `stonks`;


-- User Account Table -- 
DROP TABLE IF EXISTS `users`;
CREATE TABLE IF NOT EXISTS `users` (
  `user_id` int NOT NULL,
  `username` varchar(50) NOT NULL,
  `password` varchar(255) NOT NULL,
  PRIMARY KEY (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


INSERT INTO `users` (`user_id`, `username`, `password`) VALUES
(1, 'admin', 'admin');


-- Funds ownd by custoemr -- 
DROP TABLE IF EXISTS `funds`;
CREATE TABLE IF NOT EXISTS `funds` (
  `fund_id` int NOT NULL,
  `fund_name` varchar(50) NOT NULL,
  `fund_goals` float NOT NULL,
  `fund_investment_amount` float Not Null, 
  PRIMARY KEY (`fund_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT INTO `funds` (`fund_id`, `fund_name`, `fund_goals`,`fund_investment_amount`) VALUES
(1, 'My First Fund',40000000, 100000),
(2, 'My Second Fund', 50000000,  1000000),
(3, 'My Third Fund', 60000000,  1000000);

-- Stocks available for trade with Stonks -- 
DROP TABLE IF EXISTS `stocks`;
CREATE TABLE IF NOT EXISTS `stocks` (
  `stock_symbol` varchar (10) not null,
  `stock_name` varchar(50) NOT NULL,
  PRIMARY KEY (`stock_symbol`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT INTO `stocks` (`stock_name`, `stock_symbol`) VALUES
('YZJ Shipbldg SGD', 'BS6.SI'),
('Singtel', 'Z74.SI'),
('DBS', 'D05.SI');


-- Stocks owned by a customer -- 
-- When buying stock this table will be updated. if stock does not exist, the add. Stock price and volume will be updated--  
DROP TABLE IF EXISTS `settlements`;
CREATE TABLE IF NOT EXISTS `settlements`(
    `settlement_id` int not Null,
	`user_id` int NOT NULL,
    `stock_symbol` varchar(50) NOT NULL,
    `stock_price` float not Null,
    `volume` int not Null,
	 PRIMARY KEY (settlement_id),
     FOREIGN KEY (`user_id`) REFERENCES users(`user_id`),
	 FOREIGN KEY (`stock_symbol`) REFERENCES stocks(`stock_symbol`)
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;



INSERT INTO `settlements` (`settlement_id`, `user_id`, `stock_symbol`,`stock_price`,`volume`) VALUES
(1,1, 'BS6.SI', 0.5, 1000),
(2,1, 'Z74.SI', 3.5, 1000),
(3,1, 'D05.SI', 22.5, 1000);    



--  Fund has what stock -- 
DROP TABLE IF EXISTS `funds_settlement`;
CREATE TABLE IF NOT EXISTS `funds_settlement` (
  `fund_id` int NOT NULL,
  `settlement_id` int NOT NULL,
  PRIMARY KEY (`fund_id`,`settlement_id`),
  FOREIGN KEY (`fund_id`) REFERENCES funds(`fund_id`),
  FOREIGN KEY (`settlement_id`) REFERENCES settlements(`settlement_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT INTO `funds_settlement` (`fund_id`, `settlement_id`) VALUES
(1, 1),
(1, 2),
(1, 3);

-- Who owns which fund --
DROP TABLE IF EXISTS `users_funds`;
CREATE TABLE IF NOT EXISTS `users_funds` (
  `user_id` int NOT NULL,
  `fund_id` int NOT NULL,
  PRIMARY KEY (`user_id`,`fund_id`),
  FOREIGN KEY (`user_id`) REFERENCES users(`user_id`),
  FOREIGN KEY (`fund_id`) REFERENCES funds(`fund_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT INTO `users_funds` (`user_id`, `fund_id`) VALUES
(1, 1),
(1, 2),
(1, 3);



-- Stocks available in the marketplace this will act as the CDP -- 
DROP TABLE IF EXISTS `marketplace`;
CREATE TABLE IF NOT EXISTS `marketplace`(
    `marketplace_id` int not Null,
    `marketplace_name` varchar(50) NOT NULL,
     PRIMARY KEY (`marketplace_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

    
INSERT INTO `marketplace` (`marketplace_id`, `marketplace_name`) VALUES
(1,'Stonk Stock Exchange');

DROP TABLE IF EXISTS `marketplace_stocks`;
CREATE TABLE IF NOT EXISTS `marketplace_stocks`(
	`marketplace_id` int not Null,
    `stock_symbol` varchar(50) NOT NULL,
	`volume_in_market` int Not Null,
    PRIMARY KEY (`marketplace_id`,`stock_symbol`),
    FOREIGN KEY (`marketplace_id`) REFERENCES marketplace(`marketplace_id`),
	FOREIGN KEY (`stock_symbol`) REFERENCES stocks(`stock_symbol`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT INTO `marketplace_stocks` (`marketplace_id`, `stock_symbol`,`volume_in_market`) VALUES
(1,'BS6.SI',1000000),
(1,'Z74.SI',1000000),
(1,'D05.SI',1000000);


-- This will be an insert only table -- 
-- Store all transaction data --
DROP TABLE IF EXISTS `transactions`;
CREATE TABLE IF NOT EXISTS `transactions`(
    `transaction_id` int not Null,
	`user_id` int NOT NULL,
    `marketplace_id` int NOT NULL,
    `stock_symbol` varchar(50) NOT NULL,
    `stock_price` float not Null,
    `volume` int not Null,
    `date` datetime not null,
	PRIMARY KEY (transaction_id),
    FOREIGN KEY (`user_id`) REFERENCES users(`user_id`),
	FOREIGN KEY (`stock_symbol`) REFERENCES stocks(`stock_symbol`),
    FOREIGN KEY (`marketplace_id`) REFERENCES marketplace(`marketplace_id`)
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


-- all transactions with marketplace will be reflected here -- 
INSERT INTO `transactions` (`transaction_id`, `user_id`,`marketplace_id`, `stock_symbol`,`stock_price`,`volume`,`date`) VALUES
(1,1, 1,'BS6.SI', 0.5, 1000, '2020-01-01 00:00:00'),
(2,1, 1,'Z74.SI', 3.5, -1000, '2020-01-01 00:00:00'),
(3,1, 1,'D05.SI', 22.5, 1000, '2020-01-01 00:00:00');

