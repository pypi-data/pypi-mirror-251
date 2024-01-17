"use strict";

suite('rb/ui/views/DateInlineEditorView', function () {
  const initialDate = '2022-09-16';
  let view;
  let $container;
  beforeEach(function () {
    $container = $('<div/>').appendTo($testsScratch);
  });
  describe('Construction', function () {
    it('Default', function () {
      view = new RB.DateInlineEditorView({
        el: $container
      });
      view.render();
      expect(view.options.descriptorText).toBe(null);
      expect(view.options.minDate).toBe(null);
      expect(view.options.maxDate).toBe(null);
      expect(view.options.rawValue).toBe(null);
      expect(view.$buttons.length).toBe(1);
      expect(view.$field.length).toBe(1);
      const field = view.$field[0];
      expect(field.children.length).toBe(1);
      expect(field.firstElementChild.outerHTML).toBe('<input type="date">');
    });
    it('With options provided', function () {
      view = new RB.DateInlineEditorView({
        el: $container,
        rawValue: initialDate,
        descriptorText: 'Test',
        minDate: '2020-10-10',
        maxDate: '2030-10-10'
      });
      view.render();
      expect(view.options.descriptorText).toBe('Test');
      expect(view.options.minDate).toBe('2020-10-10');
      expect(view.options.maxDate).toBe('2030-10-10');
      expect(view.options.rawValue).toBe(initialDate);
      expect(view.$buttons.length).toBe(1);
      expect(view.$field.length).toBe(1);
      const field = view.$field[0];
      expect(field.firstChild.textContent).toBe('Test');
      expect(field.firstElementChild.outerHTML).toBe('<input type="date" max="2030-10-10" min="2020-10-10">');
    });
  });
  describe('Operations', function () {
    afterEach(function () {
      view.hideEditor();
    });
    describe('startEdit', function () {
      it('With an initial date', function () {
        view = new RB.DateInlineEditorView({
          el: $container,
          rawValue: initialDate
        });
        view.render();
        view.startEdit();
        const field = view.$field[0];
        expect(field.firstChild.tagName).toBe('INPUT');
        expect(field.firstElementChild.tagName).toBe('INPUT');
        expect(field.firstElementChild.value).toBe(initialDate);
      });
      it('With no initial date', function () {
        view = new RB.DateInlineEditorView({
          el: $container
        });
        view.render();
        view.startEdit();
        const field = view.$field[0];
        expect(field.firstChild.tagName).toBe('INPUT');
        expect(field.firstElementChild.tagName).toBe('INPUT');
        expect(field.firstElementChild.value).toBe('');
      });
      it('With a descriptor text', function () {
        view = new RB.DateInlineEditorView({
          el: $container,
          descriptorText: 'Test'
        });
        view.render();
        view.startEdit();
        const field = view.$field[0];
        expect(field.firstChild.tagName).toBe(undefined);
        expect(field.firstChild.textContent).toBe('Test');
        expect(field.firstElementChild.tagName).toBe('INPUT');
        expect(field.firstElementChild.value).toBe('');
      });
      it('With a descriptor text and initial date', function () {
        view = new RB.DateInlineEditorView({
          el: $container,
          descriptorText: 'Test',
          rawValue: initialDate
        });
        view.render();
        view.startEdit();
        const field = view.$field[0];
        expect(field.firstChild.tagName).toBe(undefined);
        expect(field.firstChild.textContent).toBe('Test');
        expect(field.firstElementChild.tagName).toBe('INPUT');
        expect(field.firstElementChild.value).toBe(initialDate);
      });
    });
    describe('save', function () {
      it('With a new date', function () {
        view = new RB.DateInlineEditorView({
          el: $container
        });
        view.render();
        view.startEdit();
        view.setValue(initialDate);
        view.save();
        expect(view.options.rawValue).toBe(initialDate);
        expect(view.$el[0].innerHTML).toBe(initialDate);
      });
      it('With an empty value', function () {
        view = new RB.DateInlineEditorView({
          el: $container,
          rawValue: initialDate
        });
        view.render();
        view.startEdit();
        view.setValue('');
        view.save();
        expect(view.options.rawValue).toBe('');
        expect(view.$el[0].innerHTML).toBe('');
      });
      it('Without any changes made', function () {
        view = new RB.DateInlineEditorView({
          el: $container,
          rawValue: initialDate
        });
        view.render();
        view.startEdit();
        view.save();
        expect(view.options.rawValue).toBe(initialDate);
        expect(view.$el[0].innerHTML).toBe('');
      });
    });
  });
  describe('Events', function () {
    it('On change', function () {
      view = new RB.DateInlineEditorView({
        el: $container
      });
      spyOn(view, '_scheduleUpdateDirtyState');
      view.render();
      view.$field.trigger('change');
      expect(view._scheduleUpdateDirtyState).toHaveBeenCalled();
    });
  });
});

//# sourceMappingURL=dateInlineEditorViewTests.js.map