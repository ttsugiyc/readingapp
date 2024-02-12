INSERT INTO user (username, email, password)
VALUES
  ('test', 't@t', 'scrypt:32768:8:1$kTM4XSyk7HsdxRGm$5532008dc90508315e98cd90cbfc9818a896faf18a834b88766d5b96ffbf017064f21dd10eb06b138dcc44259d05eca780f5796ca65084e6187855ea5fd16acd'),
  ('other', NULL, 'scrypt:32768:8:1$W6iu42BqxqUpOn8T$170384d3ccebb5b98a45c2501ae288d2678888d2fd3f4dd6ee5f5eb8ec692a72801a04c8876ac79d2694b7769d6dd2d17207a2d05517cefc94bf1a8208482d0e');

INSERT INTO book (title, isbn_13, authors, publisher, image_name)
VALUES
  ('test title', '0123456789012', 'test authors', 'test publisher', 'test_image');

INSERT INTO post (user_id, book_id, comment, status, created, modified)
VALUES
  (1, 1, 'test' || x'0a' || 'comment', 1, '2018-01-01 00:00:00', '2018-01-01 00:00:00');