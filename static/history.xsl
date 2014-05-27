<?xml version="1.0" encoding="utf-8"?>

<!-- This transformation extends history from sets of client/room id and dates.
	 Result - table with applied table.css file -->

<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
	xmlns:cl="http://www.example.com/clients"
	xmlns:ro="http://www.example.com/rooms"
	xmlns:hi="http://www.example.com/history">

	<xsl:output method="html" encoding="utf-8" />
	

<!-- Main tamplate of document node - transforms it to html page -->
	<xsl:template match="/">
		<html>
			<head>
				<title>History</title>
	        	<link href='http://fonts.googleapis.com/css?family=PT+Sans' rel='stylesheet' type='text/css'/>
	        	<link rel="stylesheet" type="text/css" href="static/table.css"/>
			</head>
			<body>
				<xsl:apply-templates/>
			</body>
		</html>
	</xsl:template>
	

<!-- Template applied to hotel node. Creates the table and fills it with data from database  -->

	<xsl:template match="hotel">
		    <h1>History</h1>				
				<table class='center'>

					<!-- Head of table created -->
					<tr>
						<td class="toupper">Dates</td>
						<td class="toupper">Client Info</td>
						<td class="toupper">Room </td>
						<td class="toupper">Payments Info</td>
					</tr>

					<!-- Every book-node is being processed and sotred by date-->

					<xsl:for-each select="hi:history/hi:book">
					<xsl:sort select="hi:dates/hi:from" data-type="number" order="descending"/>
					<tr>
						<!-- First column with date is filled -->
						<td>
							<xsl:value-of select="hi:dates/hi:from"/>
							&#160;/&#160;
							<xsl:value-of select="hi:dates/hi:from"/>
						</td>

						<!-- We bind to $client_extract variable XPath to client-node from clients database, which matches id-node from current book-node -->

						<xsl:variable name="current_client" select="/hotel/cl:clients/cl:client[cl:id = current()/hi:client_id]"/>

						<td class="noncentral">

							<!-- Client name processing depending on sex -->
							<xsl:choose>
								<xsl:when test="$current_client/@sex = 'male'">
									Mr.&#160;
								</xsl:when>
								<xsl:otherwise>
									Mrs.&#160;
								</xsl:otherwise>
							</xsl:choose>

							<!-- Client info extracted to table -->
							<xsl:value-of select="$current_client/cl:name"/>
							&#160;
							<xsl:value-of select="$current_client/cl:surname"/>
							<br/>
							Address:&#160;
							<xsl:value-of select="$current_client/cl:address"/>
						</td>

						<!-- Room info extracted to table-->
						<td class="noncentral">
							Number:&#160;<xsl:value-of select="hi:room_id"/>
							<br/>
							Type:&#160;<xsl:value-of select="/hotel/ro:rooms/ro:room[ro:room_id = current()/hi:room_id]/ro:description/ro:places/ro:type"/>
						</td>

					<!-- Payment info extracted -->
					<xsl:choose>
						<xsl:when test="hi:payment/hi:done = 'Yes'">
							<td class="positive">
								Type:&#160;<xsl:value-of select="hi:payment/hi:type"/>
								<br/>
								Total Sum:&#160;<xsl:value-of select="hi:payment/hi:total_summ"/>&#160;<xsl:value-of select="hi:payment/hi:total_summ/@currency"/>
								<br/>
								Done:&#160;<xsl:value-of select="hi:payment/hi:done"/>
								<br/>
							</td>
						</xsl:when>
						<xsl:otherwise>
							<td class="negative">
								Type:&#160;<xsl:value-of select="hi:payment/hi:type"/>
								<br/>
								Total Sum:&#160;<xsl:value-of select="hi:payment/hi:total_summ"/>&#160;<xsl:value-of select="hi:payment/hi:total_summ/@currency"/>
								<br/>
								Done:&#160;<xsl:value-of select="hi:payment/hi:done"/>
								<br/>
								<a href="/edit?">Edit</a>
								<br/>
							</td>
						</xsl:otherwise>
					</xsl:choose>
					</tr>
				</xsl:for-each>
			</table>
			<br/>
			<br/>
			<footer>
			  	<a href="/">Home</a> | 
			  	<a href="/rooms">List of rooms</a> |
		 		<a href="/newclient">Add new client</a> |  
			  	<a href="/book">Make new booking</a>
 			</footer>
  	</xsl:template>

</xsl:stylesheet>

