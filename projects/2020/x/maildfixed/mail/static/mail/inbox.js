// Wait for the DOM to fully load
document.addEventListener('DOMContentLoaded', function() 
{
  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  // By default, load the inbox
  load_mailbox('inbox');

  // Send email
  document.querySelector('#compose-form').onsubmit = function(event) 
  {
    event.preventDefault();
    send_email();
  };
});

// Compose email
function compose_email(recipient = '', subject = '', body = '') 
{
  if (typeof recipient !== 'string') 
  {
    recipient = '';
  }

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#email-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = recipient;
  document.querySelector('#compose-subject').value = subject;
  document.querySelector('#compose-body').value = body;
}

// Send email
function send_email() 
{
  fetch('/emails', 
  {
    method: 'POST',
    body: JSON.stringify(
    {
      recipients: document.querySelector('#compose-recipients').value,
      subject: document.querySelector('#compose-subject').value,
      body: document.querySelector('#compose-body').value
    })
  })
  .then(response => response.json())
  .then(result => 
  {
    // Print result
    console.log(result);
    document.querySelector('#compose-view').style.display = 'none';
    document.querySelector('#email-view').style.display = 'none';
    document.querySelector('#emails-view').style.display = 'block';
    load_mailbox('sent');
  })
}

// Load mailbox
function load_mailbox(mailbox) 
{
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#email-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  fetch(`/emails/${mailbox}`)
    .then(response => response.json())
    .then(emails => 
    {
      // Print emails
      console.log(emails);
      emails.forEach(email => 
      {
        const emailDiv = document.createElement('div');
        emailDiv.innerHTML = `
          <div class="first-row">
          <b>From: ${email.sender}</b> 
          <i>${email.timestamp} </i>
          </div>
          <br><b>Subject: </b>${email.subject} 
          `; 
        
        if (email.read) 
        {
          emailDiv.style.backgroundColor = 'lightgray';
        }
        else
        {
          emailDiv.style.backgroundColor = 'white';
        }

        emailDiv.className = 'email';
        emailDiv.addEventListener('click', () => 
        {
          load_email(email, mailbox);
        })
        document.querySelector('#emails-view').append(emailDiv);
      })
    })
}

// Load email
// Pass the mailbox variable to load_email to condition archiving
function load_email(email, mailbox) 
{
  // Show email and hide other views
  document.querySelector('#email-view').style.display = 'block';
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';

  // Show email
  fetch(`/emails/${email.id}`)
    .then(response => response.json())
    .then(emailData => 
    {
      console.log(emailData);
      document.querySelector('#email-view').innerHTML = `
      <b>From: </b>${emailData.sender} 
      <br><b>To: </b>${emailData.recipients} 
      <br><b>Subject: </b>${emailData.subject} 
      <br><b>Timestamp: </b>${emailData.timestamp}
      <br><b>Message: 
      <br></b>${emailData.body}
      <br><br>`;
      
      // Change email to read
      if (!email.read) 
      {
      fetch(`/emails/${email.id}`, 
        {
          method: 'PUT',
          body: JSON.stringify(
          {
            read: true
          })
        })
      }

    // Create reply email utility
    const reply_button = document.createElement('button');
    reply_button.className = 'btn btn-sm btn-outline-primary';
    reply_button.innerHTML = "Reply";
    reply_button.addEventListener('click', () => 
    {
      let subject = email.subject;
      if (subject.startsWith('Re: ')) 
      {
        subject = subject;
      }
      else 
      {
        subject = `Re: ${subject}`;
      }
      compose_email(emailData.sender, subject, `On ${emailData.timestamp}, ${emailData.sender} wrote: ${emailData.body}`); 
    })
    document.querySelector('#email-view').append(reply_button);

    // Create archive email utility
    if (mailbox !== 'sent') 
    {
      const archive_button = document.createElement('button');
      archive_button.className = 'btn btn-sm btn-outline-primary';
      archive_button.innerHTML = email.archived ? "Unarchive" : "Archive";
      archive_button.addEventListener('click', () => 
      {
        fetch(`/emails/${email.id}`, 
        {
           method: 'PUT',
          body: JSON.stringify(
            {
            archived: !email.archived
            })
        })
        .then(() => load_mailbox('inbox'))
      })
      document.querySelector('#email-view').append(archive_button);
    }
    })
}


