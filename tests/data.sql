INSERT INTO user (username, email, password, salt)
VALUES
  ('test', 'test@test', 'scrypt:32768:8:1$kTM4XSyk7HsdxRGm$5532008dc90508315e98cd90cbfc9818a896faf18a834b88766d5b96ffbf017064f21dd10eb06b138dcc44259d05eca780f5796ca65084e6187855ea5fd16acd', ''),
  ('other', 'other@other', 'scrypt:32768:8:1$W6iu42BqxqUpOn8T$170384d3ccebb5b98a45c2501ae288d2678888d2fd3f4dd6ee5f5eb8ec692a72801a04c8876ac79d2694b7769d6dd2d17207a2d05517cefc94bf1a8208482d0e', ''),
  ('null_email', Null, 'scrypt:32768:8:1$W6iu42BqxqUpOn8T$170384d3ccebb5b98a45c2501ae288d2678888d2fd3f4dd6ee5f5eb8ec692a72801a04c8876ac79d2694b7769d6dd2d17207a2d05517cefc94bf1a8208482d0e', '');

INSERT INTO book (title, isbn_13, authors, publisher, image_name)
VALUES
  ('title1', '0123456789012', 'authors1', 'publisher1', 'image1'),
  ('title2', '0123456789029', 'authors2', 'publisher2', 'image2'),
  ('title3', '0123456789036', 'authors3', 'publisher3', 'image3');

INSERT INTO post (user_id, book_id, comment, status)
VALUES
  (1, 1, 'test' || x'0a' || 'comment1', 1),
  (1, 2, 'comment2', 0),
  (2, 1, 'other_comment', 0);