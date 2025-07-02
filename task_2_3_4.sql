-- ЗАДАНИЕ 2 --------------------------------------------------------------------------------------------------------------------------------------------

-- 1 Название и продолжительность самого длительного трека
SELECT track_name, track_duration FROM tracks t
WHERE track_duration = (SELECT MAX(track_duration) FROM tracks)


-- 2 Название трековб продолжительность которых не менее 3,5 минут
SELECT track_name, track_duration FROM tracks t
WHERE track_duration >= '3:30'


-- 3 Названия сборниковб вышедших в период с 2018 по 2020 год включительно
-- изменяем данные столбца collection_date для того, чтобы запросы не оказались пустыми
UPDATE collections
SET collection_date = '2019-01-01'
WHERE collection_id = 3

UPDATE collections
SET collection_date = '2018-01-01'
WHERE collection_id = 1

-- сам запрос для вывода информации
SELECT collection_name, collection_date FROM collections
WHERE collection_date BETWEEN '2018-01-01' AND '2020-01-01'


-- 4 Исполнители, чье имя состоит из одного слова
SELECT artist_name FROM artists
WHERE artist_name NOT LIKE '% %' AND artist_name NOT LIKE '%&%'


-- 5 Названия треков, которые содержат слово "мой" или "my"
-- изменяем данные столбца track_name для того, чтобы запросы не оказались пустыми
UPDATE tracks
SET track_name = 'my static'
WHERE track_id = 6

-- сам запрос для вывода информации
SELECT track_name FROM tracks t 
WHERE track_name LIKE '%my%' OR track_name LIKE '%мой%'


-- ЗАДАНИЕ 3 ------------------------------------------------------------------------------------------------------------------------------------------

-- 1 Количество исполнителей в каждом жанре
SELECT g.genre_name, COUNT(DISTINCT a.artist_id) AS artist_count FROM genres g
LEFT JOIN genresartists ga ON g.genre_id = ga.genre_id
LEFT JOIN artists a ON ga.artist_id = a.artist_id
GROUP BY g.genre_name
ORDER BY artist_count DESC

-- 2 Количество треков, вошедших в альбомы 2019 - 2020 годов
-- изменяем данные столбца a.album_date для того, чтобы запросы не оказались пустыми
UPDATE albums
SET album_date = '2019-05-08'
WHERE album_id = 2

UPDATE albums
SET album_date = '2020-05-08'
WHERE album_id = 1

-- сам запрос для вывода информации;erjdtahtvjdLj,hsq ltym/ 1/
SELECT a.album_name, a.album_date, COUNT(track_id) AS track_count FROM albums a
LEFT JOIN tracks t ON a.album_id = t.album_id
WHERE a.album_date BETWEEN '2019-01-01' AND '2020-12-31'
GROUP BY a.album_name, a.album_date
ORDER BY track_count DESC


-- 3 Средняя продолжительность треков по каждому альбому
SELECT a.album_name, AVG(track_duration) AS track_avg FROM albums a
LEFT JOIN tracks t ON a.album_id = t.album_id
GROUP BY a.album_name
ORDER BY track_avg DESC

--4 Все исполнители, которые не выпустили альбомы в 2020 году
SELECT a.artist_name FROM artists a
LEFT JOIN albumsartists aa ON a.artist_id = aa.artist_id
LEFT JOIN albums ab ON aa.album_id = ab.album_id
WHERE ab.album_date NOT BETWEEN '2020-01-01' AND '2020-12-31'
GROUP BY a.artist_name
ORDER BY a.artist_name

-- 5 Названия сборников, в которых присутствует конкретный исполнитель (pink floyd)
SELECT c.collection_name FROM collections c
LEFT JOIN collectionstracks cc ON c.collection_id = cc.collection_id
LEFT JOIN tracks t ON t.track_id = cc.track_id
LEFT JOIN albums a ON a.album_id = t.album_id
LEFT JOIN albumsartists aa ON aa.album_id = a.album_id
LEFT JOIN artists at ON at.artist_id = aa.artist_id
WHERE at.artist_name = 'pink floyd'
GROUP BY c.collection_name 
ORDER BY c.collection_name


-- ЗАДАНИЕ 4 (необязательное)-------------------------------------------------------------------------------------------------------------------------------

-- 1 Названия альбомов, в которых присутствуют исполнители более чем одного жанра
-- -- изменяем данные столбца genre_id для того, чтобы запросы не оказались пустыми
UPDATE genresartists
SET genre_id = 2
WHERE artist_id = 9

-- добавляем строку в таблицу albumsartists для того, чтобы запросы не оказались пустыми
INSERT INTO albumsartists(album_id, artist_id)
VALUES (6, 8);


SELECT a.album_name, COUNT(g.genre_name) AS album_count FROM albums a
LEFT JOIN albumsartists aa ON aa.album_id = a.album_id
LEFT JOIN artists at ON at.artist_id = aa.artist_id
LEFT JOIN genresartists ga ON ga.artist_id = at.artist_id
LEFT JOIN genres g ON g.genre_id = ga.genre_id 
GROUP BY a.album_name
HAVING COUNT(g.genre_name) > 1
ORDER BY album_count

-- 2 Наименования треков, которые не входят в сборники
-- добавляем данные в таблицу tracks
INSERT INTO tracks(track_name, track_duration, album_id)
VALUES ('one of this days i gonna cut you into little pieces', '06:29', 4)

-- сам запрос для вывода данных
SELECT t.track_name FROM tracks t
LEFT JOIN collectionstracks cc ON cc.track_id = t.track_id
LEFT JOIN collections c ON c.collection_id = cc.collection_id
WHERE c.collection_name IS NULL
GROUP BY t.track_name

-- 3 Исполнитель или исполнители, написавший самый короткий по продолжительности трек, - теоретически таких треков может быть несколько
SELECT t.track_name, a.artist_name, t.track_duration AS min_time_track FROM tracks t
LEFT JOIN albums ab ON ab.album_id = t.album_id
LEFT JOIN albumsartists aa ON aa.album_id = ab.album_id 
LEFT JOIN artists a ON a.artist_id = aa.artist_id 
WHERE t.track_duration = (
	SELECT MIN(t.track_duration) FROM tracks t
	LEFT JOIN albums ab ON ab.album_id = t.album_id 
	LEFT JOIN albumsartists aa ON aa.album_id = ab.album_id 
	LEFT JOIN artists a ON a.artist_id = aa.artist_id)
GROUP BY a.artist_name, t.track_name, t.track_duration
ORDER BY min_time_track

--  4 Названия альбомов содержащих наименьшее количество треков
SELECT a.album_name, COUNT(t.track_id) AS track_count FROM albums a
JOIN tracks t ON t.album_id = a.album_id
GROUP BY a.album_id, a.album_name
HAVING COUNT(t.track_id) = (
        -- Находим минимальное количество треков
        SELECT COUNT(t2.track_id) FROM albums a2
        JOIN tracks t2 ON t2.album_id = a2.album_id
        GROUP BY a2.album_id
        ORDER BY COUNT(t2.track_id) ASC  -- Сортируем по возрастанию
        LIMIT 1  -- Берём наименьшее значение
    )
ORDER BY 
    a.album_name;

