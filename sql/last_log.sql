SELECT
	* 
FROM 
	statuslog
WHERE client_ip = "192.168.1.28"

ORDER BY
	log_time DESC
	
LIMIT 4
