  $(document).ready(function () {


      // BACK-END FUNCTIONALITY
      $(".sidenav").sidenav({
          edge: "right"
      });

      $("select").formSelect();
      $('.modal').modal();

      // https://stackoverflow.com/questions/51504878/materialize-css-modal-open-on-page-load-with-fixed-nav-not-working#51540617
      var Modalelem = document.querySelector('#disclaimer');
      var disclaimer = M.Modal.init(Modalelem, {
          dismissable: false,
          opacity: 1,
          inDuration: 0
      });
      disclaimer.open();

      // STYLE DROPDOWNS
      // type dropdown
      types = ["Normal", "Fire", "Water", "Electric", "Grass", "Ice", "Fighting",
          "Poison", "Ground", "Flying", "Psychic", "Bug", "Rock", "Ghost", "Dragon"
      ]
      types.forEach(type => {
          $(".type-select .select-wrapper .select-dropdown li span:contains(" + type + ")").addClass(
              ["type-" + type.toLowerCase(), "text-shadow"]);
      });



  });