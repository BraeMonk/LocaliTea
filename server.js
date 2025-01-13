require('dotenv').config();
const express = require('express');
const nodemailer = require('nodemailer');
const bodyParser = require('body-parser');
const cors = require('cors');
app.use(cors());

const app = express();
const port = 3001;

app.use(cors());
app.use(bodyParser.json());

const transporter = nodemailer.createTransport({
    service: 'gmail',
    auth: {
        user: process.env.EMAIL,
        pass: process.env.PASSWORD
    }
});

app.post('/send-verification-email', (req, res) => {
    const { username, email } = req.body;

    const mailOptions = {
        from: process.env.EMAIL,
        to: email,
        subject: 'Email Verification',
        text: `Hello ${username}, please verify your email by clicking the following link: http://localhost:${port}/verify-email?username=${username}`
    };

    transporter.sendMail(mailOptions, (error, info) => {
        if (error) {
            return res.status(500).send(error.toString());
        }
        res.status(200).send('Verification email sent: ' + info.response);
    });
});

app.listen(port, () => {
    console.log(`Node.js server running at http://localhost:${port}/`);
});

