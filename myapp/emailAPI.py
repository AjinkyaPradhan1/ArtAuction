def sendEmail(email,password):
    import smtplib 
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
	
    me = "ajinkyappradhan@gmail.com"
    you = email

    msg = MIMEMultipart('alternative')
    msg['Subject'] = "Verification Mail Art Auction"
    msg['From'] = me
    msg['To'] = you

    html = """<html>
  					<head></head>
  					<body>
    					<h1>Welcome to Art Auction</h1>
    					<p>Registration Successful,click the link below to verify your account</p>
    					<h2>Username : """+email+"""</h2>
    					<h2>Password : """+str(password)+"""</h2>
    					<br>
    					<a href='http://localhost:8000/verifyuser/?email="""+email+"""' >Click here to verify account</a>		
  					</body>
				</html>
    """
	
    s = smtplib.SMTP('smtp.gmail.com', 587) 
    s.starttls() 
    s.login("ajinkyappradhan@gmail.com", "ajinkya_2193027") 
	
    part2 = MIMEText(html, 'html')
    msg.attach(part2)
	
    s.sendmail(me,you,str(msg)) 
    s.quit() 
    print("Verification mail sent successfully..............")