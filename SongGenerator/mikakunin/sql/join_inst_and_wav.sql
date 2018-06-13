SELECT  
instId.instrument_name
,sound.proc_dir
FROM mst_sound_instrumentClass as inst
INNER JOIN
(
	SELECT instrument_id ,instrument_name
    FROM sound.ctl_instrument 
    WHERE instrument_name = "Bass"
)  instId
ON inst.instrument_id = instId.instrument_id 
LEFT OUTER JOIN
mst_sound as sound
ON inst.sound_id = sound.sound_id 
;