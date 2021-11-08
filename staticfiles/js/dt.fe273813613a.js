
  app.use(express.static('public'));
  app.use(express.static(__dirname + '/public'));
  app.get('/style.css', function(req, res) {
  res.sendFile(__dirname + "/" + "style.css");
});
  alert("This alert box was called with the onload event");

       $(document).ready( function () {
       $('#table_id').DataTable({

       } );
