const c = console;
/*
 * The datatables use https://datatables.net/ and are set up in this format:
 *
 *   thead   (the row with sort arrows)
 *   tfooter (the row with filters)
 *   tbody   (the data)
 *
 * Datatables can be configured to work in two modes: client-side or server-side
 * as specified by data-server-side: true|false in the HTML file
 * 
 * Server-side uses ajax calls to fetch the data upon changes to filters/search etc...
 * Cient-side does it all with the initial loaded data
 *
 */


$.fn.dataTable.Api.register("column().title()", function() {
  return $(this.header())
    .text()
    .trim();
});

$.fn.dataTable.Api.register("column().allowFilter()", function() {
  const value = $(this.header()).data("allow-filter");
  return value === undefined ? true : value;
});

$.fn.dataTable.Api.register("column().simpleFilter()", function() {
  const value = $(this.header()).data("simple-filter");
  return value === undefined ? false : value;
});

$(() => {
  const update_filters_for_server_mode = (column, distinct_values) => {
    if (distinct_values) {
      const footer = $(column.footer());
      let filterDropDown = footer.children("select");

      // Emtpy (first run?) so initialise the column....
      if (!filterDropDown.length) {
        footer.empty();
        filterDropDown = $('<select><option value="">filter</option></select>')
          .appendTo(footer)
          .on("change", function() {
            column.search($(this).val(), false, true, true).draw();
          });
      }

      // Remove all but default entry and the selected one (i.e. filter active)
      filterDropDown.children('option').not(':first').not(':selected').remove();

      // Add the values
      if (distinct_values.length != 1) {
        for (const filter_value of distinct_values) {
          filterDropDown.append($("<option>", { value: filter_value }).text(filter_value));
        }
      } else {
        if (filterDropDown.children("option").length != 2) {
          for (const filter_value of distinct_values) {
            filterDropDown.append($("<option>", { value: filter_value }).text(filter_value));
          }
        }
      }
    }
  };

  const update_column_filters_from_ajax_data = json => {
    const api = $(".data-table")
      .dataTable()
      .api();
    const columns = api.settings().init().columns;
    api.columns().every(function(column_index) {
      if (this.allowFilter()) {
        update_filters_for_server_mode(this, json.distinct_column_values[columns[column_index].data]);
      }
    });

    return json.data;
  };

  const buildFilterDropDown = (column, footer) => {
    return $('<select><option value="">filter</option></select>')
      .appendTo(footer)
      .on("change", function() {
        if (column.simpleFilter()) {
          column.search($(this).val(), false, true, true).draw();
        } else {
          const val = $.fn.dataTable.util.escapeRegex($(this).val());
          column.search(val ? "^" + val + "$" : "", true, false, false).draw();
        }
      });
  };


  const initialize_client_side_filter = (column, footer, entries) => {
    const filterDropDown = buildFilterDropDown(column, footer);
    Array.from(entries.keys())
      .sort()
      .forEach(display => {
        filterDropDown.append($("<option>", { value: display }).text(display));
      });
  };

  const initialize_client_side_column = (column, footer) => {
    const entries = new Map();
    column.nodes().each(function(element) {
      const $element = $(element);
      const display = $element.data("filter") || $element.data("sort") || $element.data("order") || $element.text().trim();
      const value = $element.text().trim();
      entries.set(display, value);
    });
    if (entries.size <= 50) {
      initialize_client_side_filter(column, footer, entries);
    }
  };

  const initialize_client_side_data_table = data_table_elem => {
    $(data_table_elem).DataTable({
      language: {
        search: "",
        searchPlaceholder: "Search"
      },
      initComplete: function() {
        this.api()
          .columns()
          .every(function() {
            const column = this;
            const footer = $(column.footer());
            footer.empty();

            if (column.allowFilter()) {
              initialize_client_side_column(column, footer);
            }
          });
      }
    });
  };

  const initialize_server_side_data_table = data_table_elem => {
    $(data_table_elem).DataTable({
      ajax: {
        url: "data_source/",
        dataSrc: update_column_filters_from_ajax_data,
        error: ajaxErrorHandler
      },
      language: {
        search: "",
        searchPlaceholder: "Search"
      }
    });
  };

  const ajaxErrorHandler = (xhr, error, thrown) => {
    // this should really be returning a 403, not a redirect to the login page
    // but for now this is the best we can do to ensure that if the request is unauthorised
    // the user is redirected to log in.
    if (error == "parsererror" || xhr.status == 403) {
      window.location = "/auth/login";
    }
  };

  // Append filters to each column. Requires a <tfoot> element.
  $(".data-table").each((data_table_index, data_table) => {
    if ($(data_table).data("serverSide")) {
      initialize_server_side_data_table(data_table);
    } else {
      initialize_client_side_data_table(data_table);
    }
  });
});
