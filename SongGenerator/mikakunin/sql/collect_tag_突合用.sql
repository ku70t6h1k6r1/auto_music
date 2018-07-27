SELECT 
userId
,messageType
,messageId
,messageText
,timestamp
FROM line_messages.sounds_production
WHERE 
userId in
(
	SELECT userId
	FROM line_messages.sounds_production 
	WHERE  1 = 1
    AND messageId = 8203689709173
    #AND messageText like '%友達からのLINEを%'
 )
 order by timestamp asc
 

