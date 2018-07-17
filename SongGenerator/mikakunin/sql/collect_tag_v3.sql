
SELECT *
FROM line_messages.sounds_production 
WHERE userId in (
	SELECT DISTINCT userId 
	FROM line_messages.sounds_production audio
	WHERE audio.messageType = 'audio'
)
and messageType in ('audio', 'text');

SELECT 
audio.timestamp as getAudioDt
,audio.messageId as audioId
,tag.timestamp as getTagDt
,tag.messageText as text
,tag.userId as user
FROM line_messages.sounds_production audio
LEFT OUTER JOIN
line_messages.sounds_production tag
ON audio.userId = tag.userId
AND audio.timestamp < tag.timestamp
WHERE audio.dt > '2018-07-02 22:00:00'
AND audio.messageType = 'audio'
AND tag.messageType = 'text'
AND audio.userId not in ('Uabc20551ecd34db1684d3a2363769c52')
ORDER BY tag.userId, audio.timestamp;




#ORDER BY userId, timestamp ASC;
