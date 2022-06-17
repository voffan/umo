/**
 * The cell type adds supports for displaing the label value except the key in the key-value
 * dropdown editor type.
 */
class KeyValueListEditor extends Handsontable.editors.HandsontableEditor {
  prepare(row, col, prop, td, value, cellProperties) {
    super.prepare(row, col, prop, td, value, cellProperties);

    Object.assign(this.htOptions, {
      data: this.cellProperties.source,
      columns: [{
          data: '_id',
        },
        {
          data: 'label',
        },
      ],
      hiddenColumns: {
        columns: [1],
      },
      colWidths: cellProperties.width - 1,
      beforeValueRender(value, {
        row,
        instance
      }) {
        return instance.getDataAtRowProp(row, 'label');
      },
    });

    if (cellProperties.keyValueListCells) {
      this.htOptions.cells = cellProperties.keyValueListCells;
    }
    if (this.htEditor) {
      this.htEditor.destroy();
    }

    this.htEditor = new Handsontable(this.htContainer, this.htOptions);
  }

  setValue(value) {
    if (this.htEditor) {
      var index = this.htEditor.getDataAtProp('_id').findIndex(id => id === value);

      if (index !== -1) {
        value = this.htEditor.getDataAtRowProp(index, 'label');
      } else {
        index = this.htEditor.getDataAtProp('label').findIndex(label => label.includes(value));
        if (index !== -1) {
            value = this.htEditor.getDataAtRowProp(index, '_id');
        }
        console.log(index);
      }
      console.log(index);
    }
    console.log(value);
    super.setValue(value);
  }

  getValue() {
    const value = super.getValue();

    if (this.htEditor) {
      const labels = this.htEditor.getDataAtProp('label');
      const row = labels.indexOf(value);

      if (row !== -1) {
        return this.htEditor.getDataAtRowProp(row, '_id');
      }
    }
    return value;
  }
}

const keyValueListValidator = function(value, callback) {
  let valueToValidate = value;

  if (valueToValidate === null || valueToValidate === void 0) {
    valueToValidate = '';
  }

  if (this.allowEmpty && valueToValidate === '') {
    callback(true);
  } else {
    callback(this.source.find(({
      _id
    }) => _id === value) ? true : false);
  }
};
const keyValueListRenderer = function(hot, TD, row, col, prop, value, cellProperties) {
  let item = NaN;
  if(!isNaN(parseInt(value))) {
    item = cellProperties.source.find(({
        _id
    }) => _id == value);
  }
  else
  {
    item = cellProperties.source.find(({
        label
    }) => label.includes(value));
  }

  if (item) {
    value = item.label;
  }

  Handsontable.renderers.getRenderer('autocomplete').call(hot, hot, TD, row, col, prop, value, cellProperties);
};

Handsontable.cellTypes.registerCellType('key-value-list', {
  editor: KeyValueListEditor,
  validator: keyValueListValidator,
  renderer: keyValueListRenderer,
});