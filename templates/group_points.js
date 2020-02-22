function adjust_height(){

}

function InitTable(table_columns, table_app){
    $('#scores_list').empty();
    var grid = new Backgrid.Grid({
        columns: table_columns,
        collection: table_app,
        className: "backgrid table table-bordered table-hover"
    });
    var $backgrid = $("#scores_list");
    $backgrid.append(grid.render().el);
    $('th.rotate>a').addClass('rotate');
}

var originalInitialize = Backgrid.HeaderCell.prototype.initialize;
Backgrid.HeaderCell.prototype.initialize = function (options) {
    originalInitialize.apply(this, arguments);
    var width = options.column.get("width");
    if (width)
    {
        this.$el.addClass(width);
    }
}

var columns=[
{
    editable: false,
    name: "fullname",
    label: "ФИО",
    cell: "string"
},
{% for course in data.courses %}
{
    editable: false,
    name: "{{ course.0 }}",
    label: "{{ course.1 }}",
    cell: {% if is_exam %} "string" {% else %} Backgrid.NumberCell.extend({ decimals:1 }) {% endif %},
    width: 'rotate'
},
{% endfor %}
]

var data=[
{% for item in data.group_points %}
{
    "fullname": "{{ item.fullname }}",
    {%for disc in item.scores %}
    "{{ disc.0 }}": {% if is_exam %} "{{disc.1}}" {% else %} {{disc.1|stringformat:".1f"}} {% endif %},
    {% endfor %}
},
{% endfor %}
]

var Application = Backbone.Model.extend({ });
var Applications = Backbone.Collection.extend({
    model: Application,
    state: {
            pageSize: 30
    },
    mode: "client" // page entirely on the client side.
});

var apps = new Applications(data);

InitTable(columns, apps);