"use strict";

suite('rb/views/FileAttachmentThumbnail', function () {
  let reviewRequest;
  let model;
  let view;
  beforeEach(function () {
    reviewRequest = new RB.ReviewRequest();
    model = new RB.FileAttachment({
      downloadURL: 'http://example.com/file.png',
      filename: 'file.png'
    });
    spyOn(model, 'trigger').and.callThrough();
  });
  describe('Rendering', function () {
    function expectElements() {
      expect(view.$('a.edit').length).toBe(1);
      expect(view.$('.file-caption').length).toBe(1);
      expect(view.$('.file-actions').length).toBe(1);
      expect(view.$('.file-delete').length).toBe(view.options.canEdit && model.get('loaded') ? 1 : 0);
      expect(view.$('.file-update').length).toBe(view.options.canEdit && model.get('loaded') ? 1 : 0);
    }
    function expectAttributeMatches() {
      expect(view.$('.file-download').attr('href')).toBe(model.get('downloadURL'));
      expect(view.$('.file-caption .edit').text()).toBe(model.get('caption'));
    }
    it('Using existing elements', function () {
      const $el = $('<div/>').addClass(RB.FileAttachmentThumbnail.prototype.className).html(RB.FileAttachmentThumbnail.prototype.template(_.defaults({
        caption: 'No caption',
        captionClass: 'edit empty-caption'
      }, model.attributes)));
      model.set('loaded', true);
      view = new RB.FileAttachmentThumbnail({
        renderThumbnail: true,
        reviewRequest: reviewRequest,
        el: $el,
        model: model
      });
      $testsScratch.append(view.$el);
      view.render();
      expectElements();
      expect(view.$('.file-actions').is(':visible')).toBe(true);
      expect(view.$('.fa-spinner').length).toBe(0);
    });
    it('Rendered thumbnail with unloaded model', function () {
      view = new RB.FileAttachmentThumbnail({
        reviewRequest: reviewRequest,
        renderThumbnail: true,
        model: model
      });
      $testsScratch.append(view.$el);
      view.render();
      expectElements();
      expect(view.$('.file-actions').children().length).toBe(0);
      expect(view.$('.fa-spinner').length).toBe(1);
    });
    describe('Rendered thumbnail with loaded model', function () {
      beforeEach(function () {
        model.id = 123;
        model.attributes.id = 123;
        model.set('caption', 'My Caption');
        model.set('loaded', true);
        model.url = '/api/file-attachments/123/';
      });
      it('With review UI', function () {
        model.set('reviewURL', '/review/');
        view = new RB.FileAttachmentThumbnail({
          reviewRequest: reviewRequest,
          renderThumbnail: true,
          model: model
        });
        $testsScratch.append(view.$el);
        view.render();
        expectElements();
        expectAttributeMatches();
        expect(view.$('.file-actions').children().length).toBe(2);
        expect(view.$('.fa-spinner').length).toBe(0);
        expect(view.$('.file-review').length).toBe(1);
        expect(view.$('.file-add-comment').length).toBe(0);
      });
      it('No review UI', function () {
        view = new RB.FileAttachmentThumbnail({
          reviewRequest: reviewRequest,
          renderThumbnail: true,
          model: model
        });
        $testsScratch.append(view.$el);
        view.render();
        expectElements();
        expectAttributeMatches();
        expect(view.$('.file-actions').children().length).toBe(2);
        expect(view.$('.fa-spinner').length).toBe(0);
        expect(view.$('.file-review').length).toBe(0);
        expect(view.$('.file-add-comment').length).toBe(1);
      });
    });
  });
  describe('Actions', function () {
    beforeEach(function () {
      model.id = 123;
      model.attributes.id = 123;
      model.set('loaded', true);
      model.url = '/api/file-attachments/123/';
      view = new RB.FileAttachmentThumbnail({
        canEdit: true,
        reviewRequest: reviewRequest,
        renderThumbnail: true,
        model: model
      });
      $testsScratch.append(view.$el);
      view.render();
      spyOn(view, 'trigger').and.callThrough();
    });
    it('Begin caption editing', function () {
      view._captionEditorView.startEdit();
      expect(view.trigger).toHaveBeenCalledWith('beginEdit');
    });
    it('Cancel caption editing', function () {
      view._captionEditorView.startEdit();
      expect(view.trigger).toHaveBeenCalledWith('beginEdit');
      view._captionEditorView.cancel();
      expect(view.trigger).toHaveBeenCalledWith('endEdit');
    });
    it('Save caption', function (done) {
      spyOn(model, 'save').and.callFake(() => {
        expect(view.trigger).toHaveBeenCalledWith('endEdit');
        expect(model.get('caption')).toBe('Foo');
        expect(model.save).toHaveBeenCalled();
        done();
      });
      view._captionEditorView.startEdit();
      expect(view.trigger).toHaveBeenCalledWith('beginEdit');
      view.$('input').val('Foo').triggerHandler('keyup');
      view._captionEditorView.submit();
    });
    it('Delete', function (done) {
      spyOn(model, 'destroy').and.callThrough();
      spyOn($, 'ajax').and.callFake(options => options.success());
      spyOn(view.$el, 'fadeOut').and.callFake(done => done());
      spyOn(view, 'remove').and.callFake(() => {
        expect($.ajax).toHaveBeenCalled();
        expect(model.destroy).toHaveBeenCalled();
        expect(model.trigger.calls.argsFor(2)[0]).toBe('destroying');
        expect(view.$el.fadeOut).toHaveBeenCalled();
        done();
      });
      view.$('.file-delete').click();
    });
  });
});

//# sourceMappingURL=fileAttachmentThumbnailViewTests.js.map