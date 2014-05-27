<?xml version="1.0" encoding="utf-8"?>


<!-- This stylesheet transform hotel.xml database to html-file with table
		containing information about rooms in table (applied table.css file)-->

<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
	xmlns:cl="http://www.example.com/clients"
	xmlns:ro="http://www.example.com/rooms"
	xmlns:hi="http://www.example.com/history">
	<xsl:output method="html" encoding="utf-8" />


	<!-- This parameter defines criterion of sorting. We will use it later
		 on our web page of hotel rooms view -->
	<!-- <xsl:param name="criterion" select="ro:price"/> -->



	<!-- Main tamplate of document node - transforms it to html page -->	
	<xsl:template match="/">
		<html>
			<head>
				<title>List of rooms offered</title>
				<link href='http://fonts.googleapis.com/css?family=PT+Sans' rel='stylesheet' type='text/css'/>
	        	<link rel="stylesheet" type="text/css" href="/static/table.css"/>
	        </head>
	        <body>
	        	<xsl:apply-templates/>
	        </body>
	    </html>
	</xsl:template>

	<!-- Template applied to hotel node. Creates the table and fills it with data from database  -->
	<xsl:template match="hotel">
		<h1>List of rooms offered</h1>			

				<table class='center'>
					<!-- Head of table created -->
					<tr>
						<td class="toupper">Room Number</td>
						<td class="toupper">Description</td>
						<td class="toupper">Price</td>
					</tr>

					<!-- Every room-node is being processed and sotred by $criterion -->
					<xsl:for-each select="ro:rooms/ro:room">
					<xsl:sort select="ro:price" data-type="text" lang="en"/>
					<tr>
						<td class="enlarged">
							<xsl:value-of select="ro:room_id"/>
						</td>
							<td class="noncentral">
								<table class="inner">
									<tr>
										<td>Floor:</td> 
										<td><xsl:value-of select="ro:description/ro:floor"/></td>
									</tr>
									<tr>
										<td>Balcony: </td>
										<td><xsl:value-of select="ro:description/ro:balcony"/></td>
									</tr>
									<tr>
										<td>Fridge: </td>
										<td><xsl:value-of select="ro:description/ro:fridge"/></td>
									</tr>
									<tr>
										<td>Conditioning: </td>
										<td><xsl:value-of select="ro:description/ro:conditioning"/></td>
									</tr>
									<tr>
										<td>Places: </td>
										<td><xsl:value-of select="ro:description/ro:places/ro:type"/></td>
									</tr>
								</table>
							</td>
							<td><xsl:value-of select="ro:price"/>
								&#160;
								<xsl:value-of select="ro:price/@currency"/>
							</td>
						</tr>
					</xsl:for-each>
				</table>
				<br/><br/>
			<footer>
			  	<a href="/">Home</a> | 
			  	<a href="/history">All clients history</a> |
		 		<a href="/newclient">Add new client</a> |  
			  	<a href="/book">Make new booking</a>
 			</footer>
  	</xsl:template>

</xsl:stylesheet>

