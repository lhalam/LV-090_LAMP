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

INSERT INTO sources (source_name, url, source_date_added, url_date_modified, rank) VALUES
('test1', 'www.google.com', '2013-06-20', NULL, 3),
('test2', 'www.test.com', '2013-06-20', NULL, 5),
('test3', 'www.bash.im', '2013-06-20', NULL, 7),
('test4', 'www.w3s.com', '2013-06-20', NULL, 2);

INSERT INTO source_to_addresses (source_id, v4_id, v6_id) VALUES
(1, 1, NULL),
(1, 2, NULL),
(2, 3, NULL),
(2, 4, NULL),
(3, 5, NULL),
(3, 6, NULL),
(4, 7, NULL);

INSERT INTO whitelist (v4_id_whitelist, v6_id_whitelist) VALUES
(3, NULL),
(4, NULL),
(7, NULL),
(8, NULL);

INSERT INTO blacklist (v4_id_blacklist, v6_id_blacklist) VALUES
(1, NULL),
(2, NULL),
(5, NULL),
(6, NULL);