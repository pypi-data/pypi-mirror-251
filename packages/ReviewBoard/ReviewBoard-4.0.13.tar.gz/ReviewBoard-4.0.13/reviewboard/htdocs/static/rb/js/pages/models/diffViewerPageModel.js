"use strict";

/**
 * The model for the diff viewer page.
 *
 * This handles all attribute storage and diff context parsing needed to
 * display and update the diff viewer.
 *
 * Model Attributes:
 *     allChunksCollapsed (boolean):
 *         Whether to collapse all chunks down to only show modified ones,
 *         instead of showing all lines in the file.
 *
 *     canDownloadDiff (boolean):
 *         Whether a diff file can be downloaded, given the current revision
 *         state.
 *
 *     canToggleExtraWhitespace (boolean):
 *         Whether the user can toggle the display of extra whitespace
 *         (mismatched indentation and trailing whitespace).
 *
 *     filenamePatterns (Array):
 *         A list of filenames or patterns used to filter the diff viewer.
 *         This is optional.
 *
 *     numDiffs (number):
 *         The total number of diffs.
 */
RB.DiffViewerPage = RB.ReviewablePage.extend({
  defaults: _.defaults({
    allChunksCollapsed: false,
    canDownloadDiff: false,
    canToggleExtraWhitespace: false,
    filenamePatterns: null,
    numDiffs: 1
  }, RB.ReviewablePage.prototype.defaults),
  /**
   * Construct the page's instance.
   *
   * This defines child objects for managing state related to the page
   * prior to parsing the provided attributes payload and initializing
   * the instance.
   *
   * NOTE: this explicitly doesn't use the shorthand "member function" syntax
   * because otherwise browsers get confused about whether this is a class
   * constructor.
   */
  constructor: function constructor() {
    this.commentsHint = new RB.DiffCommentsHint();
    this.commits = new RB.DiffCommitCollection();
    this.commitHistoryDiff = new RB.CommitHistoryDiffEntryCollection();
    this.files = new RB.DiffFileCollection();
    this.pagination = new RB.Pagination();
    this.revision = new RB.DiffRevision();
    RB.ReviewablePage.apply(this, arguments);
  },
  /**
   * Initialize the page.
   *
   * This will begin listening for events on the page and set up default
   * state.
   */
  initialize() {
    RB.ReviewablePage.prototype.initialize.apply(this, arguments);
    this.diffReviewables = new RB.DiffReviewableCollection([], {
      reviewRequest: this.get('reviewRequest')
    });
    this.diffReviewables.watchFiles(this.files);
  },
  /**
   * Parse the data for the page.
   *
   * Args:
   *     rsp (object):
   *         The payload to parse.
   *
   * Returns:
   *     object:
   *     The returned attributes.
   */
  parse(rsp) {
    const attrs = _.extend(this._parseDiffContext(rsp), RB.ReviewablePage.prototype.parse.call(this, rsp));
    if (rsp.allChunksCollapsed !== undefined) {
      attrs.allChunksCollapsed = rsp.allChunksCollapsed;
    }
    if (rsp.canToggleExtraWhitespace !== undefined) {
      attrs.canToggleExtraWhitespace = rsp.canToggleExtraWhitespace;
    }
    return attrs;
  },
  /**
   * Load a new diff from the server.
   *
   * Args:
   *     options (object):
   *         The options for the diff to load.
   *
   * Option Args:
   *     baseCommitID (number):
   *         The primary key of the base commit to base the diff off of.
   *
   *     filenames (string):
   *         A comma-separated string of filenames or filename patterns to
   *         load.
   *
   *     page (number):
   *         The page number to load. Defaults to the first page.
   *
   *     revision (number):
   *         The base revision. If displaying an interdiff, this will be
   *         the first revision in the range.
   *
   *     interdiffRevision (number):
   *         The optional interdiff revision, representing the ending
   *         revision in a range.
   *
   *     tipCommitID (number):
   *         The primary key of the tip commit to base the diff off of.
   */
  loadDiffRevision() {
    let options = arguments.length > 0 && arguments[0] !== undefined ? arguments[0] : {};
    const reviewRequestURL = this.get('reviewRequest').url();
    const queryData = [];
    if (options.revision) {
      queryData.push({
        name: 'revision',
        value: options.revision
      });
    }
    if (options.interdiffRevision) {
      queryData.push({
        name: 'interdiff-revision',
        value: options.interdiffRevision
      });
    } else {
      if (options.baseCommitID) {
        queryData.push({
          name: 'base-commit-id',
          value: options.baseCommitID
        });
      }
      if (options.tipCommitID) {
        queryData.push({
          name: 'tip-commit-id',
          value: options.tipCommitID
        });
      }
    }
    if (options.page && options.page !== 1) {
      queryData.push({
        name: 'page',
        value: options.page
      });
    }
    if (options.filenamePatterns) {
      queryData.push({
        name: 'filenames',
        value: options.filenamePatterns
      });
    }
    const url = Djblets.buildURL({
      baseURL: `${reviewRequestURL}diff-context/`,
      queryData: queryData
    });
    $.ajax(url).done(rsp => this.set(this._parseDiffContext(rsp.diff_context)));
  },
  /**
   * Parse context for a displayed diff.
   *
   * Args:
   *     rsp (object):
   *         The payload to parse.
   *
   * Returns:
   *     object:
   *     The returned attributes.
   */
  _parseDiffContext(rsp) {
    if (rsp.comments_hint) {
      this.commentsHint.set(this.commentsHint.parse(rsp.comments_hint));
    }
    if (rsp.files) {
      this.files.reset(rsp.files, {
        parse: true
      });
    }
    if (rsp.pagination) {
      this.pagination.set(this.pagination.parse(rsp.pagination));
    }
    if (rsp.revision) {
      this.revision.set(this.revision.parse(rsp.revision));
    }
    this.commitHistoryDiff.reset(rsp.commit_history_diff || [], {
      parse: true
    });
    if (rsp.commits) {
      /*
       * The RB.DiffCommitListView listens for the reset event on the
       * commits collection to trigger a render, so it must be updated
       * **after** the commit history is updated.
       */
      this.commits.reset(rsp.commits, {
        parse: true
      });
    }
    return {
      canDownloadDiff: rsp.revision && rsp.revision.interdiff_revision === null,
      filenamePatterns: rsp.filename_patterns || null,
      numDiffs: rsp.num_diffs || 0
    };
  }
});

//# sourceMappingURL=diffViewerPageModel.js.map