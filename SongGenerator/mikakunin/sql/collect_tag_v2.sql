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
AND tag.timestamp < audio.timestamp + 60000
WHERE audio.dt > '2018-07-02 22:00:00'
AND audio.messageType = 'audio'
AND tag.messageType = 'text'
ORDER BY tag.userId, audio.timestamp;