'use strict';

var DISPLAY_WIDTH = 21;

var initialState = {
  pages: [
    {
      first_line_text: '123456789012345678901',
      first_line_color: 'rgbcm WKGBCMYWRGBCMYW',
      second_line_text: '123456789012345601',
      second_line_color: 'WYMCBGRwymcBGrWYM'
    }
  ],
  display_interval: 5
};

function getHexColor(colorChar) {
  switch (colorChar) {
    case 'w':
      return '#ffffff';
    case 'r':
      return '#ff0000';
    case 'g':
      return '#00ff00';
    case 'b':
      return '#0000ff';
    case 'c':
      return '#00ffff';
    case 'm':
      return '#ff00ff';
    case 'y':
      return '#ffff00';
    default:
      return '#000000';
  }
}

function getState() {

}

function renderPages(state) {
  var resultHtml = '';
  for (var i = 0; i < state.pages.length; i++) {
    resultHtml += renderPage(state.pages[i], i);
  }
  return resultHtml;
}

function renderPage(page, index) {
  var resultHtml = '\
    <div class="panel panel-default page-panel" id="page-panel-' + index.toString() + '">\
      <div class="panel-heading">\
        <button class="btn btn-danger btn-sm delete-page">Delete</button>\
        Page ' + (index+1).toString() + '\
      </div>\
      <div class="panel-body">\
        <div class="row">\
          <div class="col-md-6">\
            <div class="form-group">\
              <label for="first_line_text" class="col-sm-3">Line 1 text</label>\
              <div class="col-sm-9">\
                <input type="text" class="form-control" name="first_line_text" value="' + page.first_line_text + '"/>\
              </div>\
            </div>\
            <div class="form-group">\
              <label for="first_line_color" class="col-sm-3">Line 1 color</label>\
              <div class="col-sm-9">\
                <input type="text" class="form-control" name="first_line_color" value="' + page.first_line_color + '"/>\
              </div>\
            </div>\
            <div class="form-group">\
              <label for="second_line_text" class="col-sm-3">Line 2 text</label>\
              <div class="col-sm-9">\
                <input type="text" class="form-control" name="second_line_text" value="' + page.second_line_text + '"/>\
              </div>\
            </div>\
            <div class="form-group">\
              <label for="second_line_color" class="col-sm-3">Line 2 color</label>\
              <div class="col-sm-9">\
                <input type="text" class="form-control" name="second_line_color" value="' + page.second_line_color + '"/>\
              </div>\
            </div>\
          </div>\
          <div class="col-md-6">\
            <label>Preview</label>\
            ' + renderDisplayPreview(page) + '\
            </div>\
          </div>\
        </div>\
      </div>\
    </div>';
  return resultHtml;
}

function renderDisplayPreview(page) {
  return '<div class="display-preview">' + renderDisplayPreviewRow(page.first_line_text, page.first_line_color)
    + renderDisplayPreviewRow(page.second_line_text, page.second_line_color) + '</div>';
}

function renderDisplayPreviewRow(text, color) {
  var resultHtml = '<div class="display-row">';
  var colorChar;
  var textChar;
  var blinkClass;
  for (var i = 0; i < DISPLAY_WIDTH; i++) {
    textChar =  (i > text.length-1) ? ' ' : text[i];
    colorChar = (i > color.length-1) ? 'k' : color[i];
    blinkClass = (colorChar === colorChar.toUpperCase()) ? ' blink' : '';
    resultHtml += '<div class="display-char' + blinkClass + '" style="color: ' + getHexColor(colorChar.toLowerCase()) + ';">' + textChar + '</div>';
  }
  resultHtml += '</div>';
  return resultHtml;
}


$(document).ready(function() {
  $('#page-panel-container').html(renderPages(initialState));
});