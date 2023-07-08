const express = require("express");
const https = require("https");

const app = express();
const port = 3000;
const id = "d0a40ec123"

app.use(express.urlencoded({extended: true}));
app.use(express.static("public"));

//const listId = "d0a40ec123";



app.get("/", (req, res) => {
   res.sendFile(__dirname + "/signup.html");
});

app.post("/", (req, res) => {
    const firstname = req.body.firstname;
    const lastname = req.body.lastname;
    const emailaddress = req.body.mail;

    const subscribingUser = {
        members: [
            {
                email_address: emailaddress,
                status: "subscribed",
                merge_fields:{
                    FNAME: firstname,
                    LNAME: lastname
                }
            }
        ]
      };
      
      const url = 'https://us17.api.mailchimp.com/3.0/lists/d0a40ec123';
      const options = {
        method: 'POST',
        auth: "test:f437ee2e3eb6e7c06fc23d8b72141a15-us1"
      };
    
    const userJsonData = JSON.stringify(subscribingUser);

    const mailchimp_request = https.request(url, options, (response)=>{

        if (response.statusCode === 200){
            res.sendFile(__dirname + "/success.html");
        }else{
            res.sendFile(__dirname + "/failure.html");
        }
        response.on("data", function(data){
           const jsonData = JSON.parse(data);
           console.log(jsonData);
        });

    });

    mailchimp_request.write(userJsonData);
    mailchimp_request.end()
    // console.log( firstname + " " +  lastname + " " + emailaddress);

});

// redirecting to home sign up page
app.post("/signup", function(req, res){
    res.redirect("/");
})


app.listen(process.env.PORT || 3000, () => {
    console.log(`server started on ${port}`);
});