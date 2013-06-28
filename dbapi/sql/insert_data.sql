INSERT INTO ipv4_addresses (address, date_added) VALUES
(4286393601, '2013-06-20'),
(2099973165, '2013-06-20'),
(3232235777, '2013-06-20'),
(3232235791, '2013-06-20'),
(16843009, '2013-06-20'),
(2102081332, '2013-06-20'),
(68772477, '2013-06-20'),
(1314208321, '2013-06-20'),
(1314273857, '2013-06-20'),
(2268029495, '2013-06-20');

INSERT INTO sources (source_name, url, source_date_added, rank) VALUES
('test1', 'www.google.com', '2013-06-20', 3),
('test2', 'www.test.com', '2013-06-20', 5),
('test3', 'www.bash.im', '2013-06-20', 7),
('test4', 'www.w3c.com', '2013-06-20', 2);

INSERT INTO source_to_addresses (source_id, v4_id) VALUES
(1, 1),
(1, 2),
(2, 3),
(2, 4),
(3, 5),
(3, 6),
(4, 7);

INSERT INTO whitelist (v4_id_whitelist) VALUES
(3),
(4),
(7),
(8);

INSERT INTO blacklist (v4_id_blacklist) VALUES
(1),
(2),
(5),
(6);
