odoo.define('custom_web_changes.custom_form_view', function(require) {
  "use strict";

  var core = require('web.core');
  var FormView = require('web.FormView');

  var _t = core._t;
  var QWeb = core.qweb;

  FormView.include({
    load_record: function(record) {
      this._super.apply(this, arguments);
      if (this.model == 'res.company') {

        console.log(this.get_fields_values().is_user_company);
        if (this.get_fields_values().is_user_company == false) {
          if (this.$buttons) {
            this.$buttons.find('.o_form_button_edit').css({
              "display": "none"
            });
          }
        } else {
          if (this.$buttons) {
            this.$buttons.find('.o_form_button_edit').css({
              "display": ""
            });

          }
        }
      }

    }

  });

});
