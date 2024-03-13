CREATE DATABASE IF NOT EXISTS taskscheduler;
USE taskscheduler;

CREATE TABLE IF NOT EXISTS tasks (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(255) NOT NULL UNIQUE,
  scheduled_time DATETIME NOT NULL,
  recurrence ENUM('ONCE', 'DAILY', 'WEEKLY', 'BIWEEKLY', 'MONTHLY', 'QUARTERLY', 'YEARLY') NULL
);

-- Insert sample data if not exists
INSERT INTO tasks (name, scheduled_time, recurrence) VALUES
('Attend coding webinar', '2024-04-10 18:00:00', 'ONCE')
ON DUPLICATE KEY UPDATE name = VALUES(name), scheduled_time = VALUES(scheduled_time), recurrence = VALUES(recurrence);

INSERT INTO tasks (name, scheduled_time, recurrence) VALUES
('Weekly Grocery Shopping', '2024-03-20 10:00:00', 'WEEKLY')
ON DUPLICATE KEY UPDATE name = VALUES(name), scheduled_time = VALUES(scheduled_time), recurrence = VALUES(recurrence);

INSERT INTO tasks (name, scheduled_time, recurrence) VALUES
('Monthly Subscription Renewal', '2024-04-01 12:00:00', 'MONTHLY')
ON DUPLICATE KEY UPDATE name = VALUES(name), scheduled_time = VALUES(scheduled_time), recurrence = VALUES(recurrence);

INSERT INTO tasks (name, scheduled_time, recurrence) VALUES
('Annual Health Checkup', '2024-05-15 09:00:00', 'YEARLY')
ON DUPLICATE KEY UPDATE name = VALUES(name), scheduled_time = VALUES(scheduled_time), recurrence = VALUES(recurrence);

INSERT INTO tasks (name, scheduled_time, recurrence) VALUES
('Daily Morning Yoga', '2024-03-25 07:30:00', 'DAILY')
ON DUPLICATE KEY UPDATE name = VALUES(name), scheduled_time = VALUES(scheduled_time), recurrence = VALUES(recurrence);

INSERT INTO tasks (name, scheduled_time, recurrence) VALUES
('Biweekly Project Meeting', '2024-03-28 14:00:00', 'BIWEEKLY')
ON DUPLICATE KEY UPDATE name = VALUES(name), scheduled_time = VALUES(scheduled_time), recurrence = VALUES(recurrence);
