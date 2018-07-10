SELECT * 
FROM line_messages.sounds_production
WHERE 
dt > '2018-07-02 22:00:22'
AND messageType in ('text', 'audio')
AND userId In
(
	SELECT userId 
	FROM line_messages.sounds_production
	WHERE messageType = 'audio'
)
ORDER BY userId, timestamp;