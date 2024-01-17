suite('rb/diffviewer/models/DiffReviewable', function() {
    let callbacks;
    let reviewRequest;

    beforeEach(function() {
        callbacks = {
            success: function() {},
            error: function() {},
            complete: function() {},
        };

        reviewRequest = new RB.ReviewRequest({
            reviewURL: '/r/1/',
        });

        spyOn(callbacks, 'success');
        spyOn(callbacks, 'error');
        spyOn(callbacks, 'complete');
    });

    describe('getRenderedDiff', function() {
        it('Without interdiffs', function() {
            const diffReviewable = new RB.DiffReviewable({
                reviewRequest: reviewRequest,
                fileDiffID: 3,
                revision: 2,
                file: new RB.DiffFile({
                    index: 4,
                }),
            });

            spyOn($, 'ajax').and.callFake(request => {
                expect(request.type).toBe('GET');
                expect(request.url).toBe(
                    '/r/1/diff/2/fragment/3/?index=4&_=' + TEMPLATE_SERIAL);

                request.success('abc');
                request.complete('abc', 'success');
            });

            diffReviewable.getRenderedDiff(callbacks);

            expect($.ajax).toHaveBeenCalled();
            expect(callbacks.success).toHaveBeenCalledWith('abc');
            expect(callbacks.complete).toHaveBeenCalledWith('abc', 'success');
            expect(callbacks.error).not.toHaveBeenCalled();
        });

        it('With interdiffs', function() {
            const diffReviewable = new RB.DiffReviewable({
                reviewRequest: reviewRequest,
                fileDiffID: 3,
                revision: 2,
                interdiffRevision: 3,
                file: new RB.DiffFile({
                    index: 4,
                }),
            });

            spyOn($, 'ajax').and.callFake(request => {
                expect(request.type).toBe('GET');
                expect(request.url).toBe(
                    '/r/1/diff/2-3/fragment/3/?index=4&_=' + TEMPLATE_SERIAL);

                request.success('abc');
                request.complete('abc', 'success');
            });

            diffReviewable.getRenderedDiff(callbacks);

            expect($.ajax).toHaveBeenCalled();
            expect(callbacks.success).toHaveBeenCalledWith('abc');
            expect(callbacks.complete).toHaveBeenCalledWith('abc', 'success');
            expect(callbacks.error).not.toHaveBeenCalled();
        });

        it('With base FileDiff', function() {
            const diffReviewable = new RB.DiffReviewable({
                reviewRequest: reviewRequest,
                fileDiffID: 3,
                revision: 2,
                baseFileDiffID: 1,
                file: new RB.DiffFile({
                    index: 4,
                }),
            });

            spyOn($, 'ajax').and.callFake(request => {
                expect(request.type).toBe('GET');
                expect(request.url).toBe(
                    '/r/1/diff/2/fragment/3/?base-filediff-id=1&index=4&_=' +
                    TEMPLATE_SERIAL);

                request.success('abc');
                request.complete('abc', 'success');
            });

            diffReviewable.getRenderedDiff(callbacks);

            expect(callbacks.success).toHaveBeenCalledWith('abc');
            expect(callbacks.complete).toHaveBeenCalledWith('abc', 'success');
            expect(callbacks.error).not.toHaveBeenCalled();
        });
    });

    describe('getRenderedDiffFragment', function() {
        it('Without interdiffs', function() {
            const diffReviewable = new RB.DiffReviewable({
                reviewRequest: reviewRequest,
                fileDiffID: 3,
                revision: 2,
                file: new RB.DiffFile({
                    index: 5,
                }),
            });

            spyOn($, 'ajax').and.callFake(request => {
                expect(request.type).toBe('GET');
                expect(request.url).toBe(
                    '/r/1/diff/2/fragment/3/chunk/4/?index=5&' +
                    'lines-of-context=6&_=' + TEMPLATE_SERIAL);

                request.success('abc');
                request.complete('abc', 'success');
            });

            diffReviewable.getRenderedDiffFragment({
                chunkIndex: 4,
                linesOfContext: 6,
            }, callbacks);

            expect($.ajax).toHaveBeenCalled();
            expect(callbacks.success).toHaveBeenCalledWith('abc');
            expect(callbacks.complete).toHaveBeenCalledWith('abc', 'success');
            expect(callbacks.error).not.toHaveBeenCalled();
        });

        it('With interdiffs', function() {
            const diffReviewable = new RB.DiffReviewable({
                reviewRequest: reviewRequest,
                fileDiffID: 3,
                revision: 2,
                interdiffRevision: 3,
                interFileDiffID: 4,
                file: new RB.DiffFile({
                    index: 5,
                }),
            });

            spyOn($, 'ajax').and.callFake(request => {
                expect(request.type).toBe('GET');
                expect(request.url).toBe(
                    '/r/1/diff/2-3/fragment/3-4/chunk/4/?index=5&' +
                    'lines-of-context=6&_=' + TEMPLATE_SERIAL);

                request.success('abc');
                request.complete('abc', 'success');
            });

            diffReviewable.getRenderedDiffFragment({
                chunkIndex: 4,
                linesOfContext: 6,
            }, callbacks);

            expect($.ajax).toHaveBeenCalled();
            expect(callbacks.success).toHaveBeenCalledWith('abc');
            expect(callbacks.complete).toHaveBeenCalledWith('abc', 'success');
            expect(callbacks.error).not.toHaveBeenCalled();
        });

        it('With base filediff ID', function() {
            const diffReviewable = new RB.DiffReviewable({
                reviewRequest: reviewRequest,
                baseFileDiffID: 123,
                fileDiffID: 3,
                revision: 2,
                interdiffRevision: 3,
                interFileDiffID: 4,
                file: new RB.DiffFile({
                    index: 5,
                }),
            });

            spyOn($, 'ajax').and.callFake(request => {
                expect(request.type).toBe('GET');
                expect(request.url).toBe(
                    '/r/1/diff/2-3/fragment/3-4/chunk/4/' +
                    '?base-filediff-id=123&index=5&' +
                    'lines-of-context=6&_=' + TEMPLATE_SERIAL);

                request.success('abc');
                request.complete('abc', 'success');
            });

            diffReviewable.getRenderedDiffFragment({
                chunkIndex: 4,
                linesOfContext: 6,
            }, callbacks);

            expect($.ajax).toHaveBeenCalled();
            expect(callbacks.success).toHaveBeenCalledWith('abc');
            expect(callbacks.complete).toHaveBeenCalledWith('abc', 'success');
            expect(callbacks.error).not.toHaveBeenCalled();
        });

        it('With base filediff ID', function() {
            const diffReviewable = new RB.DiffReviewable({
                reviewRequest: reviewRequest,
                baseFileDiffID: 123,
                fileDiffID: 3,
                revision: 2,
                interdiffRevision: 3,
                interFileDiffID: 4,
                file: new RB.DiffFile({
                    index: 5,
                }),
            });

            spyOn($, 'ajax').and.callFake(request => {
                expect(request.type).toBe('GET');
                expect(request.url).toBe(
                    '/r/1/diff/2-3/fragment/3-4/chunk/4/' +
                    '?base-filediff-id=123&index=5&' +
                    'lines-of-context=6&_=' + TEMPLATE_SERIAL);

                request.success('abc');
                request.complete('abc', 'success');
            });

            diffReviewable.getRenderedDiffFragment({
                chunkIndex: 4,
                linesOfContext: 6,
            }, callbacks);

            expect($.ajax).toHaveBeenCalled();
            expect(callbacks.success).toHaveBeenCalledWith('abc');
            expect(callbacks.complete).toHaveBeenCalledWith('abc', 'success');
            expect(callbacks.error).not.toHaveBeenCalled();
        });
    });
});
