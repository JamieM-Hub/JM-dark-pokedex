  $(document).ready(function () {


      // BACK-END FUNCTIONALITY
      $(".sidenav").sidenav({
          edge: "right"
      });

      $("select").formSelect();
      $('.modal').modal();

      // STYLE DROPDOWNS
      // type dropdown
      types = ["Normal", "Fire", "Water", "Electric", "Grass", "Ice", "Fighting",
          "Poison", "Ground", "Flying", "Psychic", "Bug", "Rock", "Ghost", "Dragon"
      ]
      types.forEach(type => {
          $(".select-dropdown li span:contains(" + type + ")").addClass(
              ["type-" + type.toLowerCase(), "text-shadow"]);
      });



  });