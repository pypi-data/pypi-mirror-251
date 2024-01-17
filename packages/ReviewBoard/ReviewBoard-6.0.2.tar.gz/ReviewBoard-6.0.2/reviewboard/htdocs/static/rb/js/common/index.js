(function (global, factory) {
    typeof exports === 'object' && typeof module !== 'undefined' ? factory(exports, require('@beanbag/spina')) :
    typeof define === 'function' && define.amd ? define(['exports', '@beanbag/spina'], factory) :
    (global = typeof globalThis !== 'undefined' ? globalThis : global || self, factory(global.RB = global.RB || {}, global.Spina));
})(this, (function (exports, spina) { 'use strict';

    var _class$g;

    /**
     * Attributes for the Action model.
     *
     * Version Added:
     *     6.0
     */

    /**
     * Base model for actions.
     *
     * Subclasses may add their own attributes by passing in their own attribute
     * interface when extending this.
     *
     * Version Added:
     *     6.0
     */
    let Action = spina.spina(_class$g = class Action extends spina.BaseModel {
      static defaults = {
        actionId: '',
        visible: false
      };
    }) || _class$g;

    var _class$f;

    /**
     * Attributes for the MenuAction model.
     *
     * Version Added:
     *     6.0
     */

    /**
     * Base model for menu actions.
     *
     * Version Added:
     *     6.0
     */
    let MenuAction = spina.spina(_class$f = class MenuAction extends Action {
      static defaults = {
        children: []
      };
    }) || _class$f;

    var _class$e;
    /**
     * Base view for actions.
     *
     * Version Added:
     *     6.0
     */
    let ActionView = spina.spina(_class$e = class ActionView extends spina.BaseView {}) || _class$e;

    var _class$d, _class2$1;

    /**
     * Base class for menu actions.
     *
     * Version Added:
     *     6.0
     */
    let MenuActionView = spina.spina(_class$d = class MenuActionView extends ActionView {
      static events = {
        'focusout': 'onFocusOut',
        'keydown': 'onKeyDown',
        'mouseenter': 'openMenu',
        'mouseleave': 'closeMenu',
        'touchstart': 'onTouchStart'
      };

      /**********************
       * Instance variables *
       **********************/

      /** The menu view. */

      /**
       * Render the view.
       */
      onInitialRender() {
        this.menu = new RB.MenuView({
          $controller: this.$el
        });
        this.$el.append(this.menu.render().$el);
        const page = RB.PageManager.getPage();
        for (const childId of this.model.get('children')) {
          if (childId === '--') {
            this.menu.addSeparator();
          } else {
            const childActionView = page.getActionView(childId);
            if (childActionView) {
              this.menu.addItem({
                $child: childActionView.$el
              });
              if (childActionView.model.get('visible')) {
                childActionView.$el.show();
              }
            } else {
              console.error('Unable to find action for %s', childId);
            }
          }
        }
      }

      /**
       * Open the menu.
       */
      openMenu() {
        if (this.menu.el.children.length > 0) {
          this.menu.open({
            animate: true
          });
        }
      }

      /**
       * Close the menu.
       */
      closeMenu() {
        if (this.menu.el.children.length > 0) {
          this.menu.close({
            animate: true
          });
        }
      }

      /**
       * Handle a focus-out event.
       *
       * If the keyboard focus has moved to something outside of the menu, close
       * it.
       *
       * Args:
       *     evt (FocusEvent):
       *         The event object.
       */
      onFocusOut(evt) {
        evt.stopPropagation();

        /*
         * Only close the menu if the focus has moved to something outside of
         * this component.
         */
        const currentTarget = evt.currentTarget;
        if (!currentTarget.contains(evt.relatedTarget)) {
          this.menu.close({
            animate: false
          });
        }
      }

      /**
       * Handle a key-down event.
       *
       * When the menu has focus, this will take care of handling keyboard
       * operations, allowing the menu to be opened or closed. Opening the menu
       * will transfer the focus to the menu items.
       *
       * Args:
       *     evt (KeyboardEvent):
       *         The keydown event.
       */
      onKeyDown(evt) {
        if (evt.key === ' ' || evt.key === 'ArrowDown' || evt.key === 'ArrowUp' || evt.key === 'Enter') {
          this.menu.open({
            animate: false
          });
          this.menu.focusFirstItem();
          evt.stopPropagation();
          evt.preventDefault();
        } else if (evt.key === 'Escape') {
          this.menu.close({
            animate: false
          });
          evt.stopPropagation();
          evt.preventDefault();
        }
      }

      /**
       * Handle a touchstart event.
       *
       * Args:
       *     e (TouchEvent):
       *         The touch event.
       */
      onTouchStart(e) {
        e.stopPropagation();
        e.preventDefault();
        if (this.menu.isOpen) {
          this.closeMenu();
        } else {
          this.openMenu();
        }
      }
    }) || _class$d;

    /**
     * Base class for an action within a menu.
     *
     * This handles event registration for the click and touch events in order to
     * behave properly on both desktop and mobile.
     *
     * Version Added:
     *     6.0
     */
    let MenuItemActionView = spina.spina(_class2$1 = class MenuItemActionView extends ActionView {
      static events = {
        'click': '_onClick',
        'touchstart': '_onTouchStart'
      };

      /**
       * Handle a click event.
       *
       * Args:
       *     e (MouseEvent):
       *         The event.
       */
      _onClick(e) {
        e.stopPropagation();
        e.preventDefault();
        this.activate();
      }

      /**
       * Handle a touchstart event.
       */
      _onTouchStart() {
        /*
         * For touch events, we explicitly let the event bubble up so that the
         * parent menu can close.
         */
        this.activate();
      }

      /**
       * Activate the action.
       */
      activate() {
        // This is expected to be overridden by subclasses.
      }
    }) || _class2$1;

    const Actions = {
      Action,
      ActionView,
      MenuAction,
      MenuActionView,
      MenuItemActionView
    };

    var _class$c;

    /**
     * The base class used for Review Board collections.
     *
     * This is a thin subclass over Backbone.Collection that just provides
     * some useful additional abilities.
     */
    let BaseCollection = spina.spina(_class$c = class BaseCollection extends spina.BaseCollection {
      /**
       * Fetch models from the server.
       *
       * This behaves just like Backbone.Collection.fetch, except it
       * takes a context parameter for callbacks and can return promises.
       *
       * Version Changed:
       *     5.0:
       *     This method was changed to return a promise. Using callbacks instead
       *     of the promise is deprecated, and will be removed in Review Board
       *     6.0.
       *
       * Args:
       *     options (object):
       *         Options for the fetch operation.
       *
       *     context (object):
       *         Context to be used when calling callbacks.
       *
       * Returns:
       *     Promise:
       *     A promise which resolves when the fetch operation is complete.
       */
      fetch() {
        let options = arguments.length > 0 && arguments[0] !== undefined ? arguments[0] : {};
        let context = arguments.length > 1 && arguments[1] !== undefined ? arguments[1] : undefined;
        if (_.isFunction(options.success) || _.isFunction(options.error)) {
          console.warn('RB.BaseCollection.fetch was called using ' + 'callbacks. Callers should be updated to use ' + 'promises instead.');
          return RB.promiseToCallbacks(options, context, newOptions => this.fetch(newOptions));
        }
        return new Promise((resolve, reject) => {
          super.fetch(_.defaults({
            error: (model, xhr, options) => reject(new BackboneError(model, xhr, options)),
            success: result => resolve(result)
          }, options));
        });
      }

      /**
       * Handle all AJAX communication for the collection.
       *
       * Backbone.js will internally call the model's sync function to
       * communicate with the server, which usually uses Backbone.sync.
       *
       * This will parse error response from Review Board so we can provide
       * a more meaningful error callback.
       *
       * Args:
       *     method (string):
       *         The HTTP method to use for the AJAX request.
       *
       *     model (object):
       *         The model to sync.
       *
       *     options (object):
       *         Options for the sync operation.
       */
      sync(method, model) {
        let options = arguments.length > 2 && arguments[2] !== undefined ? arguments[2] : {};
        return Backbone.sync.call(this, method, model, _.defaults({
          error: (xhr, textStatus, errorThrown) => {
            RB.storeAPIError(xhr);
            if (_.isFunction(options.error)) {
              options.error(xhr, textStatus, errorThrown);
            }
          }
        }, options));
      }
    }) || _class$c;

    var _class$b;
    /**
     * Base collection for resource models.
     *
     * ResourceCollection handles the fetching of models from resource lists
     * in the API.
     *
     * It can do pagination by using fetchNext/fetchPrev. Callers can check
     * hasNext/hasPrev to determine if they've reached the end.
     *
     * To fetch one page at a time, use fetch(). This can take an optional
     * starting point.
     *
     * Use fetchAll to automatically paginate through all items and store them
     * all within the collection.
     */
    let ResourceCollection = spina.spina(_class$b = class ResourceCollection extends BaseCollection {
      /**********************
       * Instance variables *
       **********************/

      /** The parent resource of the collection. */

      /** Extra data to send with the HTTP request. */

      /** The number of results to fetch at a time. */

      /** Whether there is a previous page that can be fetched. */
      hasPrev = false;

      /** Whether there is a next page that can be fetched. */
      hasNext = false;

      /** The current page to fetch. */
      currentPage = 0;

      /** The total number of results, if available. */

      /** The URL to use when fetching. */
      _fetchURL = null;

      /** The links returned by the resource. */

      /**
       * Initialize the collection.
       *
       * Args:
       *     models (Array of object):
       *         Initial set of models for the collection.
       *
       *     options (object):
       *         Options for the collection.
       *
       * Option Args:
       *     parentResource (RB.BaseResource):
       *         The parent API resource.
       *
       *     extraQueryData (object):
       *         Additional attributes to include in the API request query
       *         string.
       */
      initialize(models, options) {
        this.parentResource = options.parentResource;
        this.extraQueryData = options.extraQueryData;
        this.maxResults = options.maxResults;

        /*
         * Undefined means "we don't know how many results there are."
         * This is a valid value when parsing the payload later. It
         * may also be a number.
         */
        this.totalResults = undefined;
        this._fetchURL = null;
        this._links = null;
      }

      /**
       * Return the URL for fetching models.
       *
       * This will make use of a URL provided by fetchNext/fetchPrev/fetchAll,
       * if provided.
       *
       * Otherwise, this will try to get the URL from the parent resource.
       *
       * Returns:
       *     string:
       *     The URL to fetch.
       */
      url() {
        if (this._fetchURL) {
          return this._fetchURL;
        }
        if (this.parentResource) {
          const links = this.parentResource.get('links');
          const listKey = _.result(this.model.prototype, 'listKey');
          const link = links[listKey];
          return link ? link.href : null;
        }
        return null;
      }

      /**
       * Parse the results from the list payload.
       *
       * Args:
       *     rsp (object):
       *         The response from the server.
       *
       *     options (ResourceCollectionParseOptions):
       *         The options that were used for the fetch operation.
       */
      parse(rsp) {
        let options = arguments.length > 1 && arguments[1] !== undefined ? arguments[1] : {};
        const listKey = _.result(this.model.prototype, 'listKey');
        this._links = rsp.links || null;
        this.totalResults = rsp.total_results;
        if (options.fetchingAll) {
          this.hasPrev = false;
          this.hasNext = false;
          this.currentPage = 0;
        } else {
          this.totalResults = rsp.total_results;
          this.hasPrev = this._links !== null && this._links.prev !== undefined;
          this.hasNext = this._links !== null && this._links.next !== undefined;
          this.currentPage = options.page;
        }
        return rsp[listKey];
      }

      /**
       * Fetch models from the list.
       *
       * By default, this will replace the list of models in this collection.
       * That can be changed by providing `reset: false` in options.
       *
       * The first page of resources will be fetched unless options.start is
       * set. The value is the start position for the number of objects, not
       * pages.
       *
       * Version Changed:
       *     5.0:
       *     Deprecated callbacks and added a promise return value.
       *
       * Args:
       *     options (ResourceCollectionFetchOptions):
       *         Options for the fetch operation.
       *
       *     context (object):
       *         Context to be used when calling callbacks.
       */
      async fetch() {
        let options = arguments.length > 0 && arguments[0] !== undefined ? arguments[0] : {};
        let context = arguments.length > 1 && arguments[1] !== undefined ? arguments[1] : undefined;
        if (_.isFunction(options.success) || _.isFunction(options.error) || _.isFunction(options.complete)) {
          console.warn('RB.ResourceCollection.fetch was called using ' + 'callbacks. Callers should be updated to use ' + 'promises instead.');
          return RB.promiseToCallbacks(options, context, newOptions => this.fetch(newOptions));
        }
        const data = _.extend({}, options.data);
        if (options.start !== undefined) {
          data.start = options.start;
        }

        /*
         * There's a couple different ways that the max number of results
         * can be specified. We'll want to support them all.
         *
         * If a value is passed in extraQueryData, it takes precedence.
         * We'll just set it further down. Otherwise, options.maxResults
         * will be used if passed, falling back on the maxResults passed
         * during collection construction.
         */
        if (!this.extraQueryData || this.extraQueryData['max-results'] === undefined) {
          if (options.maxResults !== undefined) {
            data['max-results'] = options.maxResults;
          } else if (this.maxResults) {
            data['max-results'] = this.maxResults;
          }
        }
        if (options.reset === undefined) {
          options.reset = true;
        }

        /*
         * Versions of Backbone prior to 1.1 won't respect the reset option,
         * instead requiring we use 'remove'. Support this for compatibility,
         * until we move to Backbone 1.1.
         */
        options.remove = options.reset;
        const expandedFields = this.model.prototype.expandedFields;
        if (expandedFields.length > 0) {
          data.expand = expandedFields.join(',');
        }
        if (this.extraQueryData) {
          _.defaults(data, this.extraQueryData);
        }
        options.data = data;
        if (this.parentResource) {
          await this.parentResource.ready();
        }
        await super.fetch(options);
      }

      /**
       * Fetch the previous batch of models from the resource list.
       *
       * This requires hasPrev to be true, from a prior fetch.
       *
       * The collection's list of models will be replaced with the new list
       * after the fetch succeeds. Each time fetchPrev is called, the collection
       * will consist only of that page's batch of models. This can be overridden
       * by providing `reset: false` in options.
       *
       * Version Changed:
       *     5.0:
       *     Deprecated callbacks and added a promise return value.
       *
       * Args:
       *     options (ResourceCollectionFetchOptions):
       *         Options for the fetch operation.
       *
       *     context (object):
       *         Context to bind when calling callbacks.
       *
       * Returns:
       *     Promise:
       *     A promise which resolves when the operation is complete.
       */
      fetchPrev() {
        let options = arguments.length > 0 && arguments[0] !== undefined ? arguments[0] : {};
        let context = arguments.length > 1 && arguments[1] !== undefined ? arguments[1] : undefined;
        if (_.isFunction(options.success) || _.isFunction(options.error) || _.isFunction(options.complete)) {
          console.warn('RB.ResourceCollection.fetchPrev was called using ' + 'callbacks. Callers should be updated to use ' + 'promises instead.');
          return RB.promiseToCallbacks(options, context, newOptions => this.fetchPrev(newOptions));
        }
        if (!this.hasPrev) {
          return Promise.resolve();
        }
        this._fetchURL = this._links.prev.href;
        return this.fetch(_.defaults({
          page: this.currentPage - 1
        }, options));
      }

      /**
       * Fetch the next batch of models from the resource list.
       *
       * This requires hasNext to be true, from a prior fetch.
       *
       * The collection's list of models will be replaced with the new list
       * after the fetch succeeds. Each time fetchNext is called, the collection
       * will consist only of that page's batch of models. This can be overridden
       * by providing `reset: false` in options.
       *
       * Version Changed:
       *     5.0:
       *     Deprecated callbacks and added a promise return value.
       *
       * Args:
       *     options (ResourceCollectionFetchOptions):
       *         Options for the fetch operation.
       *
       *     context (object):
       *         Context to bind when calling callbacks.
       *
       * Returns:
       *     Promise:
       *     A promise which resolves when the operation is complete.
       */
      fetchNext() {
        let options = arguments.length > 0 && arguments[0] !== undefined ? arguments[0] : {};
        let context = arguments.length > 1 && arguments[1] !== undefined ? arguments[1] : undefined;
        if (_.isFunction(options.success) || _.isFunction(options.error) || _.isFunction(options.complete)) {
          console.warn('RB.ResourceCollection.fetchNext was called using ' + 'callbacks. Callers should be updated to use ' + 'promises instead.');
          return RB.promiseToCallbacks(options, context, newOptions => this.fetchNext(newOptions));
        }
        if (!this.hasNext && options.enforceHasNext !== false) {
          return Promise.resolve();
        }
        this._fetchURL = this._links.next.href;
        return this.fetch(_.defaults({
          page: this.currentPage + 1
        }, options));
      }

      /**
       * Fetch all models from the resource list.
       *
       * This will fetch all the models from a resource list on a server,
       * paginating automatically until all models are fetched. The result is
       * a list of models on the server.
       *
       * This differs from fetch/fetchPrev/fetchNext, which will replace the
       * collection each time a page of resources are loaded.
       *
       * This can end up slowing down the server. Use it carefully.
       *
       * Version Changed:
       *     5.0:
       *     Deprecated callbacks and added a promise return value.
       *
       * Args:
       *     options (ResourceCollectionFetchOptions):
       *         Options for the fetch operation.
       *
       *     context (object):
       *         Context to bind when calling callbacks.
       *
       * Returns:
       *     Promise:
       *     A promise which resolves when the operation is complete.
       */
      async fetchAll() {
        let options = arguments.length > 0 && arguments[0] !== undefined ? arguments[0] : {};
        let context = arguments.length > 1 && arguments[1] !== undefined ? arguments[1] : undefined;
        if (_.isFunction(options.success) || _.isFunction(options.error) || _.isFunction(options.complete)) {
          console.warn('RB.ResourceCollection.fetchNext was called using ' + 'callbacks. Callers should be updated to use ' + 'promises instead.');
          return RB.promiseToCallbacks(options, context, newOptions => this.fetchAll(newOptions));
        }
        const fetchOptions = _.defaults({
          enforceHasNext: false,
          fetchingAll: true,
          maxResults: 50,
          reset: false
        }, options);
        this._fetchURL = null;
        this.reset();
        await this.fetch(fetchOptions);
        while (this._links.next) {
          await this.fetchNext(fetchOptions);
        }
      }

      /**
       * Prepare the model for the collection.
       *
       * This overrides Collection's _prepareModel to ensure that the resource
       * has the proper parentObject set.
       *
       * Returns:
       *     Backbone.Model:
       *     The new model.
       */
      _prepareModel(attributes, options) {
        const model = super._prepareModel(attributes, options);
        model.set('parentObject', this.parentResource);
        return model;
      }
    }) || _class$b;

    var _class$a;

    /**
     * A model for holding a resource's extra data.
     *
     * Contains utility methods for serializing it.
     */
    let ExtraData = spina.spina(_class$a = class ExtraData extends spina.BaseModel {
      /**
       * JSONify the extra data.
       *
       * The extra data is serialized such that each key is prefixed with
       * "extra_data." so that the API can understand it. The result of this
       * function should be merged into the serialization of the parent object.
       *
       * Returns:
       *     object:
       *     An object suitable for serializing to JSON.
       */
      toJSON() {
        const data = {};
        for (const [key, value] of Object.entries(this.attributes)) {
          data[`extra_data.${key}`] = value;
        }
        return data;
      }
    }) || _class$a;

    /**
     * A mixin to add a new extra data API to a model.
     *
     * The model this is attached to gains an extraData property that is backed by
     * the extraData key of the model's attributes object. This new API also
     * enhances the model such that extraData object can be interacted with on in a
     * key-value manner instead of dealing with the whole object.
     *
     * Any class that inherits this mixin should call _setupExtraData in its
     * initialize function to ensure that the mixin will work properly. This will
     * set up the property and event listeners.
     */
    const ExtraDataMixin = {
      /**
       * Set up the resource to add the new extra data API.
       *
       * This function should be called in the model's initialize function.
       *
       * This adds an extraData attribute that is backed by the model's
       * attribute.extraData. This new model.extraData can be used directly in a
       * model.extraData.get/set fashion to get or set individual keys in the
       * extra data, instead of getting and setting the extra data all at once.
       *
       * This will also set up event listeners so that changes to extraData
       * through the ExtraData instance will trigger changed events on the
       * model itself
       */
      _setupExtraData() {
        this.extraData = new ExtraData();
        this.extraData.attributes = this.attributes.extraData;
        this.listenTo(this.extraData, 'change', this._onExtraDataChanged);
      },
      /**
       * Set the key to the value with the given options.
       *
       * This is a special case of Backbone.Model's set which does some extra
       * work when dealing with a extraData member. It ensures that extraData is
       * only ever set to an instance of ExtraData and sets up a listener
       * to fire change events when the extraData fires a change event.
       *
       * Args:
       *     key (string):
       *         The key to set.
       *
       *     value (*):
       *         The value to set.
       *
       *     options (object):
       *         Options for the set operation.
       *
       * Returns:
       *     ExtraDataMixin:
       *     This object, for chaining.
       */
      set(key, value, options) {
        let attrs;
        if (_.isObject(key)) {
          attrs = key;
          options = value;
        } else {
          attrs = {};
          attrs[key] = value;
        }
        const useExtraData = _.has(attrs, 'extraData') && _.has(this, 'extraData');
        if (useExtraData) {
          if (attrs.extraData instanceof ExtraData) {
            /*
             * We don't want to assign an ExtraData instance to the
             * model's extraData attribute because it expects a plain
             * JavaScript object.
             */
            attrs.extraData = _.clone(attrs.extraData.attributes);
          }
        }
        Backbone.Model.prototype.set.call(this, attrs, options);
        if (useExtraData) {
          this.extraData.attributes = this.attributes.extraData;
        }
        return this;
      },
      /**
       * Handle a change event fired from the model's extra data.
       *
       * This fires both the change and change:extraData for this model.
       *
       * Args:
       *     extraData (object):
       *         The key:value mapping for the extra data.
       *
       *     options (object):
       *         Options to pass along to event handlers.
       */
      _onExtraDataChanged(extraData, options) {
        this.trigger('change:extraData', this, extraData, options);
        this.trigger('change', this, options);
      },
      /**
       * Get the key from the model's extra data.
       *
       * This should only be used when the model has an extraData attribute.
       *
       * Args:
       *     key (string):
       *         The key to fetch.
       *
       * Returns:
       *     *:
       *     The value of the data.
       */
      getExtraData(key) {
        return this.extraData.get(key);
      },
      /**
       * Set the key in the model's extra data to the value.
       *
       * This should only be used when the model has an extraData attribute.
       *
       * Args:
       *     key (string):
       *         The key to set.
       *
       *     value (*):
       *         The value to set.
       */
      setExtraData(key, value) {
        this.extraData.set(key, value);
      }
    };

    /**
     * JSON serialization helpers for API resources.
     */

    /** Resource state to use for serializer methods. */

    /**
     * Serialize only if the resource is not loaded.
     *
     * Args:
     *     value (unknown):
     *         The value to serialize.
     *
     *     state (SerializerState):
     *         The resource state.
     */
    function onlyIfUnloaded(value, state) {
      return state.loaded ? undefined : value;
    }

    /**
     * Serialize only if the resource is not loaded and the value exists.
     *
     * Args:
     *     value (unknown):
     *         The value to serialize.
     *
     *     state (SerializerState):
     *         The resource state.
     */
    function onlyIfUnloadedAndValue(value, state) {
      if (!state.loaded && value) {
        return value;
      } else {
        return undefined;
      }
    }

    /**
     * Serialize only if the value exists.
     *
     * Args:
     *     value (unknown):
     *         The value to serialize.
     *
     *     state (SerializerState):
     *         The resource state.
     */
    function onlyIfValue(value) {
      return value || undefined;
    }

    /**
     * Serialize only if the resource has not yet been created on the server.
     *
     * Args:
     *     value (unknown):
     *         The value to serialize.
     *
     *     state (SerializerState):
     *         The resource state.
     */
    function onlyIfNew(value, state) {
      return state.isNew ? value : undefined;
    }

    /**
     * Serializer for text type fields.
     *
     * Args:
     *     value (unknown):
     *         The value to serialize.
     *
     *     state (SerializerState):
     *         The resource state.
     */
    function textType(value) {
      return value ? 'markdown' : 'plain';
    }

    const serializers = /*#__PURE__*/Object.defineProperty({
        __proto__: null,
        onlyIfNew,
        onlyIfUnloaded,
        onlyIfUnloadedAndValue,
        onlyIfValue,
        textType
    }, Symbol.toStringTag, { value: 'Module' });

    var _dec$6, _class$9;

    /** A link within the resource tree. */

    /**
     * The base model for all API-backed resource models.
     *
     * This provides a common set of attributes and functionality for working
     * with Review Board's REST API. That includes fetching data for a known
     * resource, creating resources, saving, deleting, and navigating children
     * resources by way of a payload's list of links.
     *
     * Other resource models are expected to extend this. In particular, they
     * should generally be extending toJSON() and parse().
     */
    let BaseResource = (_dec$6 = spina.spina({
      mixins: [ExtraDataMixin],
      prototypeAttrs: ['attrToJsonMap', 'deserializedAttrs', 'deserializers', 'expandedFields', 'extraQueryArgs', 'rspNamespace', 'serializedAttrs', 'serializers', 'supportsExtraData', 'urlIDAttr']
    }), _dec$6(_class$9 = class BaseResource extends spina.BaseModel {
      static strings = {
        INVALID_EXTRADATA_TYPE: 'extraData must be an object or undefined',
        INVALID_EXTRADATA_VALUE_TYPE: 'extraData.{key} must be null, a number, boolean, or string',
        UNSET_PARENT_OBJECT: 'parentObject must be set'
      };

      /** The key for the namespace for the object's payload in a response. */
      static rspNamespace = '';

      /** The attribute used for the ID in the URL. */
      static urlIDAttr = 'id';

      /** The list of fields to expand in resource payloads. */
      static expandedFields = [];

      /**
       * Extra query arguments for GET requests.
       *
       * This may also be a function that returns the extra query arguments.
       *
       * These values can be overridden by the caller when making a request.
       * They function as defaults for the queries.
       */
      static extraQueryArgs = {};

      /** Whether or not extra data can be associated on the resource. */
      static supportsExtraData = false;

      /**
       * A map of attribute names to resulting JSON field names.
       *
       * This is used to auto-generate a JSON payload from attribute names
       * in toJSON().
       *
       * It's also needed if using attribute names in any save({attrs: [...]})
       * calls.
       */
      static attrToJsonMap = {};

      /** A list of attributes to serialize in toJSON(). */
      static serializedAttrs = [];

      /** A list of attributes to deserialize in parseResourceData(). */
      static deserializedAttrs = [];

      /** Special serializer functions called in toJSON(). */
      static serializers = {};

      /** Special deserializer functions called in parseResourceData(). */
      static deserializers = {};

      /**
       * Return default values for the model attributes.
       *
       * Returns:
       *     object:
       *     The attribute defaults.
       */
      defaults() {
        return {
          extraData: {},
          links: null,
          loaded: false,
          parentObject: null
        };
      }

      /**
       * Return the key to use when accessing the list resource.
       *
       * Returns:
       *     string:
       *     The name of the key to use when loading data from the list resource.
       */
      listKey() {
        return this.rspNamespace + 's';
      }

      /**
       * Initialize the model.
       */
      initialize() {
        if (this.supportsExtraData) {
          this._setupExtraData();
        }
      }

      /**
       * Return the URL for this resource's instance.
       *
       * If this resource is loaded and has a URL to itself, that URL will
       * be returned. If not yet loaded, it'll try to get it from its parent
       * object, if any.
       *
       * Returns:
       *     string:
       *     The URL to use when fetching the resource. If the URL cannot be
       *     determined, this will return null.
       */
      url() {
        let links = this.get('links');
        if (links) {
          return links.self.href;
        }
        const parentObject = this.get('parentObject');
        if (parentObject) {
          links = parentObject.get('links');
          if (links) {
            const key = _.result(this, 'listKey');
            const link = links[key];
            if (link) {
              const baseURL = link.href;
              return this.isNew() ? baseURL : baseURL + this.get(this.urlIDAttr) + '/';
            }
          }
        }
        return null;
      }

      /**
       * Call a function when the object is ready to use.
       *
       * An object is ready it has an ID and is loaded, or is a new resource.
       *
       * When the object is ready, options.ready() will be called. This may
       * be called immediately, or after one or more round trips to the server.
       *
       * If we fail to load the resource, objects.error() will be called instead.
       *
       * Version Changed:
       *     5.0:
       *     Deprecated callbacks and changed to return a promise.
       *
       * Args:
       *     options (ReadyOptions):
       *         Options for the fetch operation.
       *
       *     context (object):
       *         Context to bind when executing callbacks.
       *
       * Returns:
       *     Promise:
       *     A promise which resolves when the operation is complete.
       */
      async ready() {
        let options = arguments.length > 0 && arguments[0] !== undefined ? arguments[0] : {};
        let context = arguments.length > 1 && arguments[1] !== undefined ? arguments[1] : undefined;
        if (_.isFunction(options.success) || _.isFunction(options.error) || _.isFunction(options.complete) || _.isFunction(options.ready)) {
          console.warn('BaseResource.ready was called using callbacks. ' + 'Callers should be updated to use promises instead.');
          return RB.promiseToCallbacks(options, context, () => this.ready());
        }
        const parentObject = this.get('parentObject');
        if (!this.get('loaded')) {
          if (!this.isNew()) {
            // Fetch data from the server
            await this.fetch({
              data: options.data
            });
          } else if (parentObject) {
            /*
             * This is a new object, which means there's nothing to fetch
             * from the server, but we still need to ensure that the
             * parent is loaded in order for it to have valid links.
             */
            await parentObject.ready();
          }
        }
      }

      /**
       * Call a function when we know an object exists server-side.
       *
       * This works like ready() in that it's used to delay operating on the
       * resource until we have a server-side representation. Unlike ready(),
       * it will attempt to create it if it doesn't exist first.
       *
       * If we fail to create the object, options.error() will be called
       * instead.
       *
       * Version Changed:
       *     5.0:
       *     Deprecated callbacks and added a promise return value.
       *
       * Args:
       *     options (object, optional):
       *         Object with success and error callbacks.
       *
       *     context (object, optional):
       *         Context to bind when executing callbacks.
       *
       * Returns:
       *     Promise:
       *     A promise which resolves when the operation is complete.
       */
      async ensureCreated() {
        let options = arguments.length > 0 && arguments[0] !== undefined ? arguments[0] : {};
        let context = arguments.length > 1 && arguments[1] !== undefined ? arguments[1] : undefined;
        if (_.isFunction(options.success) || _.isFunction(options.error) || _.isFunction(options.complete)) {
          console.warn('BaseResource.ensureCreated was called using ' + 'callbacks. Callers should be updated to use ' + 'promises instead.');
          return RB.promiseToCallbacks(options, context, () => this.ensureCreated());
        }
        await this.ready();
        if (!this.get('loaded')) {
          await this.save();
        }
      }

      /**
       * Fetch the object's data from the server.
       *
       * An object must have an ID before it can be fetched. Otherwise,
       * options.error() will be called.
       *
       * If this has a parent resource object, we'll ensure that's ready before
       * fetching this resource.
       *
       * The resource must override the parse() function to determine how
       * the returned resource data is parsed and what data is stored in
       * this object.
       *
       * Version Changed:
       *     5.0:
       *     Deprecated the callbacks and added a promise return value.
       *
       * Args:
       *     options (object, optional):
       *         Options to pass through to the base Backbone fetch operation.
       *
       *     context (object, optional):
       *         Context to bind when executing callbacks.
       *
       * Returns:
       *     Promise:
       *     A promise which resolves when the operation is complete.
       */
      async fetch() {
        let options = arguments.length > 0 && arguments[0] !== undefined ? arguments[0] : {};
        let context = arguments.length > 1 && arguments[1] !== undefined ? arguments[1] : undefined;
        if (_.isFunction(options.success) || _.isFunction(options.error) || _.isFunction(options.complete)) {
          console.warn('BaseResource.fetch was called using callbacks. ' + 'Callers should be updated to use promises instead.');
          return RB.promiseToCallbacks(options, context, newOptions => this.fetch(newOptions));
        }
        if (this.isNew()) {
          throw new Error('fetch cannot be used on a resource without an ID');
        }
        const parentObject = this.get('parentObject');
        if (parentObject) {
          await parentObject.ready();
        }
        return new Promise((resolve, reject) => {
          super.fetch(_.extend({
            error: (model, xhr, options) => reject(new BackboneError(model, xhr, options)),
            success: () => resolve()
          }, options));
        });
      }

      /**
       * Save the object's data to the server.
       *
       * If the object has an ID already, it will be saved to its known
       * URL using HTTP PUT. If it doesn't have an ID, it will be saved
       * to its parent list resource using HTTP POST
       *
       * If this has a parent resource object, we'll ensure that's created
       * before saving this resource.
       *
       * An object must either be loaded or have a parent resource linking to
       * this object's list resource URL for an object to be saved.
       *
       * The resource must override the toJSON() function to determine what
       * data is saved to the server.
       *
       * If we successfully save the resource, options.success() will be
       * called, and the "saved" event will be triggered.
       *
       * If we fail to save the resource, options.error() will be called.
       *
       * Version Changed:
       *     5.0:
       *     Deprecated the callbacks and added a promise return value.
       *
       * Args:
       *     options (object, optional):
       *         Options for the save operation.
       *
       *     context (object, optional):
       *         Context to bind when executing callbacks.
       *
       * Returns:
       *     Promise:
       *     A promise which resolves when the operation is complete.
       */
      async save() {
        let options = arguments.length > 0 && arguments[0] !== undefined ? arguments[0] : {};
        let context = arguments.length > 1 && arguments[1] !== undefined ? arguments[1] : undefined;
        if (_.isFunction(options.success) || _.isFunction(options.error) || _.isFunction(options.complete)) {
          console.warn('BaseResource.save was called using callbacks. ' + 'Callers should be updated to use promises instead.');
          return RB.promiseToCallbacks(options, context, newOptions => this.save(newOptions));
        }
        this.trigger('saving', options);
        await this.ready();
        const parentObject = this.get('parentObject');
        if (parentObject) {
          await parentObject.ensureCreated();
        }
        return this._saveObject(options);
      }

      /**
       * Handle the actual saving of the object's state.
       *
       * This is called internally by save() once we've handled all the
       * readiness and creation checks of this object and its parent.
       *
       * Args:
       *     options (object):
       *         Options for the save operation.
       *
       * Returns:
       *     Promise:
       *     A promise which resolves when the operation is complete.
       */
      _saveObject(options) {
        return new Promise((resolve, reject) => {
          const url = _.result(this, 'url');
          if (!url) {
            reject(new Error('The object must either be loaded from the server or ' + 'have a parent object before it can be saved'));
            return;
          }
          const saveOptions = _.defaults({
            error: (model, xhr, options) => {
              this.trigger('saveFailed', options);
              reject(new BackboneError(model, xhr, options));
            },
            success: (model, xhr) => {
              this.trigger('saved', options);
              resolve(xhr);
            }
          }, options);
          saveOptions.attrs = options.attrs || this.toJSON(options);
          const files = [];
          const readers = [];
          if (!options.form) {
            if (this.payloadFileKeys && window.File) {
              /* See if there are files in the attributes we're using. */
              this.payloadFileKeys.forEach(key => {
                const file = saveOptions.attrs[key];
                if (file) {
                  files.push(file);
                }
              });
            }
          }
          if (files.length > 0) {
            files.forEach(file => {
              const reader = new FileReader();
              readers.push(reader);
              reader.onloadend = () => {
                const ready = readers.every(r => r.readyState === FileReader.DONE);
                if (ready) {
                  this._saveWithFiles(files, readers, saveOptions);
                }
              };
              reader.readAsArrayBuffer(file);
            });
          } else {
            super.save({}, saveOptions);
          }
        });
      }

      /**
       * Save the model with a file upload.
       *
       * When doing file uploads, we need to hand-structure a form-data payload
       * to the server. It will contain the file contents and the attributes
       * we're saving. We can then call the standard save function with this
       * payload as our data.
       *
       * Args:
       *     files (Array of object):
       *         A list of files, with ``name`` and ``type`` keys.
       *
       *     fileReaders (Array of FileReader):
       *         Readers corresponding to each item in ``files``.
       *
       *     options (SaveWithFilesOptions):
       *         Options for the save operation.
       */
      _saveWithFiles(files, fileReaders, options) {
        const boundary = options.boundary || '-----multipartformboundary' + new Date().getTime();
        const blob = [];
        for (const [key, file, reader] of _.zip(this.payloadFileKeys, files, fileReaders)) {
          if (!file || !reader) {
            continue;
          }
          blob.push('--' + boundary + '\r\n');
          blob.push('Content-Disposition: form-data; name="' + key + '"; filename="' + file.name + '"\r\n');
          blob.push('Content-Type: ' + file.type + '\r\n');
          blob.push('\r\n');
          blob.push(reader.result);
          blob.push('\r\n');
        }
        for (const [key, value] of Object.entries(options.attrs)) {
          if (!this.payloadFileKeys.includes(key) && value !== undefined && value !== null) {
            blob.push('--' + boundary + '\r\n');
            blob.push('Content-Disposition: form-data; name="' + key + '"\r\n');
            blob.push('\r\n');
            blob.push(value + '\r\n');
          }
        }
        blob.push('--' + boundary + '--\r\n\r\n');
        super.save({}, _.extend({
          contentType: 'multipart/form-data; boundary=' + boundary,
          data: new Blob(blob),
          processData: false
        }, options));
      }

      /**
       * Delete the object's resource on the server.
       *
       * An object must either be loaded or have a parent resource linking to
       * this object's list resource URL for an object to be deleted.
       *
       * Version Changed:
       *     5.0:
       *     Deprecated callbacks and changed to return a promise.
       *
       * Args:
       *     options (object, optional):
       *         Object with success and error callbacks.
       *
       *     context (object, optional):
       *         Context to use when calling callbacks.
       *
       * Returns:
       *     Promise:
       *     A promise which resolves when the operation is complete.
       */
      async destroy() {
        let options = arguments.length > 0 && arguments[0] !== undefined ? arguments[0] : {};
        let context = arguments.length > 1 && arguments[1] !== undefined ? arguments[1] : undefined;
        if (_.isFunction(options.success) || _.isFunction(options.error) || _.isFunction(options.complete)) {
          console.warn('BaseResource.destroy was called using ' + 'callbacks. Callers should be updated to use ' + 'promises instead.');
          return RB.promiseToCallbacks(options, context, newOptions => this.destroy(newOptions));
        }
        this.trigger('destroying', options);
        const parentObject = this.get('parentObject');
        if (!this.isNew() && parentObject) {
          /*
           * XXX This is temporary to support older-style resource
           *     objects. We should just use ready() once we're moved
           *     entirely onto BaseResource.
           */
          await parentObject.ready();
        }
        await this._destroyObject(options);
      }

      /**
       * Set up the deletion of the object.
       *
       * This is called internally by destroy() once we've handled all the
       * readiness and creation checks of this object and its parent.
       *
       * Once we've done some work to ensure the URL is valid and the object
       * is ready, we'll finish destruction by calling _finishDestroy.
       *
       * Args:
       *     options (object):
       *         Options object to include with events.
       *
       * Returns:
       *     Promise:
       *     A promise which resolves when the operation is complete.
       */
      async _destroyObject() {
        let options = arguments.length > 0 && arguments[0] !== undefined ? arguments[0] : {};
        const url = _.result(this, 'url');
        if (url) {
          await this.ready();
          await this._finishDestroy(options);
        } else {
          if (this.isNew()) {
            /*
             * If both this resource and its parent are new, it's
             * possible that we'll get through here without a url. In
             * this case, all the data is still local to the client
             * and there's not much to clean up; just call
             * Model.destroy and be done with it.
             */
            await this._finishDestroy(options);
          } else {
            throw new Error('The object must either be loaded from the server ' + 'or have a parent object before it can be deleted');
          }
        }
      }

      /**
       * Finish destruction of the object.
       *
       * This will call the parent destroy method, then reset the state
       * of the object on success.
       *
       * Args:
       *     options (object):
       *         Object with success and error callbacks.
       *
       * Returns:
       *     Promise:
       *     A promise which resolves when the operation is complete.
       */
      _finishDestroy(options) {
        return new Promise((resolve, reject) => {
          const parentObject = this.get('parentObject');
          super.destroy({
            error: (model, xhr, options) => reject(new BackboneError(model, xhr, options)),
            success: () => {
              /*
               * Reset the object so it's new again, but with the same
               * parentObject.
               */
              this.set(_.defaults({
                id: null,
                parentObject: parentObject
              }, _.result(this, 'defaults')));
              this.trigger('destroyed', options);
              resolve();
            },
            wait: true
          });
        });
      }

      /**
       * Parse and returns the payload from an API response.
       *
       * This will by default only return the object's ID and list of links.
       * Subclasses should override this to return any additional data that's
       * needed, but they must include the results of
       * BaseResource.protoype.parse as well.
       *
       * Args:
       *     rsp (object):
       *         The payload received from the server.
       *
       * Returns:
       *     object:
       *     Attributes to set on the model.
       */
      parse(rsp) {
        console.assert(this.rspNamespace, 'rspNamespace must be defined on the resource model');
        if (rsp.stat !== undefined) {
          /*
           * This resource payload is inside an envelope from an API
           * call. It's not model construction data or from a list
           * resource.
           */
          rsp = rsp[this.rspNamespace];
        }
        return _.defaults({
          extraData: rsp.extra_data,
          id: rsp.id,
          links: rsp.links,
          loaded: true
        }, this.parseResourceData(rsp));
      }

      /*
       * Parse the resource data from a payload.
       *
       * By default, this will make use of attrToJsonMap and any
       * jsonDeserializers to construct a resulting set of attributes.
       *
       * This can be overridden by subclasses.
       *
       * Args:
       *     rsp (object):
       *         The payload received from the server.
       *
       * Returns:
       *     object:
       *     Attributes to set on the model.
       */
      parseResourceData(rsp) {
        const attrs = {};
        for (const attrName of this.deserializedAttrs) {
          const deserializer = this.deserializers[attrName];
          const jsonField = this.attrToJsonMap[attrName] || attrName;
          let value = rsp[jsonField];
          if (deserializer) {
            value = deserializer.call(this, value);
          }
          if (value !== undefined) {
            attrs[attrName] = value;
          }
        }
        return attrs;
      }

      /**
       * Serialize and return object data for the purpose of saving.
       *
       * When saving to the server, the only data that will be sent in the
       * API PUT/POST call will be the data returned from toJSON().
       *
       * This will build the list based on the serializedAttrs, serializers,
       * and attrToJsonMap properties.
       *
       * Subclasses can override this to create custom serialization behavior.
       *
       * Args:
       *     options (object):
       *         Options for the save operation.
       *
       * Returns:
       *     object:
       *     The serialized data.
       */
      toJSON(options) {
        const serializerState = {
          isNew: this.isNew(),
          loaded: this.get('loaded')
        };
        const data = {};
        for (const attrName of this.serializedAttrs) {
          const serializer = this.serializers[attrName];
          let value = this.get(attrName);
          if (serializer) {
            value = serializer.call(this, value, serializerState);
          }
          const jsonField = this.attrToJsonMap[attrName] || attrName;
          data[jsonField] = value;
        }
        if (this.supportsExtraData) {
          _.extend(data, this.extraData.toJSON());
        }
        return data;
      }

      /**
       * Handle all AJAX communication for the model and its subclasses.
       *
       * Backbone.js will internally call the model's sync function to
       * communicate with the server, which usually uses Backbone.sync.
       *
       * We wrap this to convert the data to encoded form data (instead
       * of Backbone's default JSON payload).
       *
       * We also parse the error response from Review Board so we can provide
       * a more meaningful error callback.
       *
       * Args:
       *     method (string):
       *         The HTTP method to use.
       *
       *     model (Backbone.Model):
       *         The model to sync.
       *
       *     options (SyncOptions):
       *         Options for the operation.
       */
      sync(method, model) {
        let options = arguments.length > 2 && arguments[2] !== undefined ? arguments[2] : {};
        let data;
        let contentType;
        if (method === 'read') {
          data = options.data || {};
          const extraQueryArgs = _.result(this, 'extraQueryArgs', {});
          if (!_.isEmpty(extraQueryArgs)) {
            data = _.extend({}, extraQueryArgs, data);
          }
        } else {
          if (options.form) {
            data = null;
          } else if (options.attrs && !_.isArray(options.attrs)) {
            data = options.attrs;
          } else {
            data = model.toJSON(options);
            if (options.attrs) {
              data = _.pick(data, options.attrs.map(attr => this.attrToJsonMap[attr] || attr));
            }
          }
          contentType = 'application/x-www-form-urlencoded';
        }
        const syncOptions = _.defaults({}, options, {
          /* Use form data instead of a JSON payload. */
          contentType: contentType,
          data: data,
          processData: true
        });
        if (!options.form && this.expandedFields.length > 0) {
          syncOptions.data.expand = this.expandedFields.join(',');
        }
        syncOptions.error = (xhr, textStatus, jqXHR) => {
          RB.storeAPIError(xhr);
          const rsp = xhr.errorPayload;
          if (rsp && _.has(rsp, this.rspNamespace)) {
            /*
             * The response contains the current version of the object,
             * which we want to preserve, in case it did any partial
             * updating of data.
             */
            this.set(this.parse(rsp));
          }
          if (_.isFunction(options.error)) {
            options.error(xhr, textStatus, jqXHR);
          }
        };
        return Backbone.sync.call(this, method, model, syncOptions);
      }

      /**
       * Perform validation on the attributes of the resource.
       *
       * By default, this validates the extraData field, if provided.
       *
       * Args:
       *     attrs (object):
       *         The attributes to validate.
       *
       * Returns:
       *     string:
       *     An error string or ``undefined``.
       */
      validate(attrs) {
        if (this.supportsExtraData && attrs.extraData !== undefined) {
          const strings = BaseResource.strings;
          if (!_.isObject(attrs.extraData)) {
            return strings.INVALID_EXTRADATA_TYPE;
          }
          for (const [key, value] of Object.entries(attrs.extraData)) {
            if (!_.isNull(value) && (!_.isNumber(value) || _.isNaN(value)) && !_.isBoolean(value) && !_.isString(value)) {
              return strings.INVALID_EXTRADATA_VALUE_TYPE.replace('{key}', key);
            }
          }
        }
      }
    }) || _class$9);

    /** Mixin for resources that are children of a draft resource. */

    /**
     * Mixin for resources that are children of a draft resource.
     *
     * This will ensure that the draft is in a proper state before operating
     * on the resource.
     */
    const DraftResourceChildModelMixin = {
      /**
       * Delete the object's resource on the server.
       *
       * This will ensure the draft is created before deleting the object,
       * in order to record the deletion as part of the draft.
       *
       * Args:
       *     options (object, optional):
       *         Options for the operation, including callbacks.
       *
       *     context (object, optional):
       *         Context to bind when calling callbacks.
       *
       * Returns:
       *     Promise:
       *     A promise which resolves when the operation is complete.
       */
      async destroy() {
        let options = arguments.length > 0 && arguments[0] !== undefined ? arguments[0] : {};
        let context = arguments.length > 1 && arguments[1] !== undefined ? arguments[1] : undefined;
        if (_.isFunction(options.success) || _.isFunction(options.error) || _.isFunction(options.complete)) {
          console.warn('RB.DraftResourceChildModelMixin.destroy was ' + 'called using callbacks. Callers should be updated ' + 'to use promises instead.');
          return RB.promiseToCallbacks(options, context, newOptions => this.destroy(newOptions));
        }
        await this.get('parentObject').ensureCreated();
        await _super(this).destroy.call(this, options);
      },
      /**
       * Call a function when the object is ready to use.
       *
       * This will ensure the draft is created before ensuring the object
       * is ready.
       *
       * Version Changed:
       *     5.0:
       *     Deprecated callbacks and changed to return a promise.
       *
       * Args:
       *     options (object, optional):
       *         Options for the operation, including callbacks.
       *
       *     context (object, optional):
       *         Context to bind when calling callbacks.
       *
       * Returns:
       *     Promise:
       *     A promise which resolves when the operation is complete.
       */
      async ready() {
        let options = arguments.length > 0 && arguments[0] !== undefined ? arguments[0] : {};
        let context = arguments.length > 1 && arguments[1] !== undefined ? arguments[1] : undefined;
        if (_.isFunction(options.success) || _.isFunction(options.error) || _.isFunction(options.complete) || _.isFunction(options.ready)) {
          console.warn('RB.DraftResourceChildModelMixin.ready was ' + 'called using callbacks. Callers should be updated ' + 'to use promises instead.');
          return RB.promiseToCallbacks(options, context, newOptions => this.ready());
        }
        await this.get('parentObject').ensureCreated();
        await _super(this).ready.call(this);
      }
    };

    var _dec$5, _class$8;

    /**
     * States for file attachments.
     *
     * This coincides with
     * :py:class:`reviewboard.reviews.models.review_request.FileAttachmentState`.
     *
     * Version Added:
     *     6.0
     */
    exports.FileAttachmentStates = void 0;

    /**
     * Attributes for the FileAttachment model.
     *
     * Version Added:
     *     6.0
     */
    (function (FileAttachmentStates) {
      FileAttachmentStates["DELETED"] = "deleted";
      FileAttachmentStates["DRAFT"] = "draft";
      FileAttachmentStates["NEW"] = "new";
      FileAttachmentStates["NEW_REVISION"] = "new-revision";
      FileAttachmentStates["PENDING_DELETION"] = "pending-deletion";
      FileAttachmentStates["PUBLISHED"] = "published";
    })(exports.FileAttachmentStates || (exports.FileAttachmentStates = {}));
    /**
     * Represents a new or existing file attachment.
     */
    let FileAttachment = (_dec$5 = spina.spina({
      prototypeAttrs: ['attrToJsonMap', 'deserializedAttrs', 'payloadFileKeys', 'rspNamespace', 'serializedAttrs', 'serializers', 'supportsExtraData']
    }), _dec$5(_class$8 = class FileAttachment extends BaseResource {
      /**
       * Return default values for the model attributes.
       *
       * Returns:
       *     object:
       *     The attribute defaults.
       */
      defaults() {
        return _.defaults({
          'attachmentHistoryID': null,
          'caption': null,
          'downloadURL': null,
          'file': null,
          'filename': null,
          'publishedCaption': null,
          'reviewURL': null,
          'revision': null,
          'state': exports.FileAttachmentStates.NEW,
          'thumbnailHTML': null
        }, super.defaults());
      }
      static rspNamespace = 'file_attachment';
      static payloadFileKeys = ['path'];
      static supportsExtraData = true;
      static attrToJsonMap = {
        attachmentHistoryID: 'attachment_history_id',
        downloadURL: 'url',
        file: 'path',
        reviewURL: 'review_url',
        thumbnailHTML: 'thumbnail'
      };
      static serializedAttrs = ['attachmentHistoryID', 'caption', 'file'];
      static deserializedAttrs = ['attachmentHistoryID', 'caption', 'downloadURL', 'filename', 'publishedCaption', 'reviewURL', 'revision', 'state', 'thumbnailHTML'];
      static serializers = {
        'attachmentHistoryID': onlyIfNew,
        'file': onlyIfNew
      };
    }) || _class$8);

    var _dec$4, _class$7;

    /**
     * A file attachment that's part of a draft.
     */
    let DraftFileAttachment = (_dec$4 = spina.spina({
      mixins: [DraftResourceChildModelMixin],
      prototypeAttrs: ['rspNamespace']
    }), _dec$4(_class$7 = class DraftFileAttachment extends FileAttachment {
      static rspNamespace = 'draft_file_attachment';
    }) || _class$7);

    /**
     * Mixin for resources that have special "draft" URLs.
     */



    /**
     * Options for the ready operation.
     *
     * Version Added:
     *     6.0
     */

    /**
     * Mixin for resources that have special "draft" URLs.
     *
     * Some resources contain a "draft/" singleton URL that will either redirect to
     * the URL for an existing draft, or indicate there's no draft (and requiring
     * that one be created).
     *
     * These resources need a little more logic to look up the draft state and
     * craft the proper URL. They can use this mixin to do that work for them.
     */
    const DraftResourceModelMixin = {
      /**
       * Call a function when the object is ready to use.
       *
       * If the object is unloaded, we'll likely need to grab the draft
       * resource, particularly if we haven't already retrieved a draft.
       *
       * Otherwise, we delegate to the parent's ready().
       *
       * Version Changed:
       *     5.0:
       *     Deprecated callbacks and changed to return a promise.
       *
       * Args:
       *     options (object, optional):
       *         Options for the operation, including callbacks.
       *
       *     context (object, optional):
       *         Context to bind when calling callbacks.
       *
       * Returns:
       *     Promise:
       *     A promise which resolves when the operation is complete.
       */
      async ready() {
        let options = arguments.length > 0 && arguments[0] !== undefined ? arguments[0] : {};
        let context = arguments.length > 1 && arguments[1] !== undefined ? arguments[1] : undefined;
        if (_.isFunction(options.success) || _.isFunction(options.error) || _.isFunction(options.complete) || _.isFunction(options.ready)) {
          console.warn('RB.DraftResourceModelMixin.ready was ' + 'called using callbacks. Callers should be updated ' + 'to use promises instead.');
          return RB.promiseToCallbacks(options, context, newOptions => this.ready(newOptions));
        }
        if (!this.get('loaded') && this.isNew() && this._needDraft === undefined) {
          this._needDraft = true;
        }
        await _super(this).ready.call(this, options);
        if (this._needDraft) {
          /*
           * Start by delegating to the parent ready() function. Because the
           * object is "new", this will make sure that the parentObject is
           * ready.
           */
          await this._retrieveDraft(options);
        }
      },
      /**
       * Destroy the object.
       *
       * If destruction is successful, we'll reset the needDraft state so we'll
       * look up the draft the next time an operation is performed.
       *
       * Version Changed:
       *     5.0:
       *     Deprecated callbacks and changed to return a promise.
       *
       * Args:
       *     options (object, optional):
       *         Options for the operation, including callbacks.
       *
       *     context (object, optional):
       *         Context to bind when calling callbacks.
       *
       * Returns:
       *     Promise:
       *     A promise which resolves when the operation is complete.
       */
      async destroy() {
        let options = arguments.length > 0 && arguments[0] !== undefined ? arguments[0] : {};
        let context = arguments.length > 1 && arguments[1] !== undefined ? arguments[1] : undefined;
        if (_.isFunction(options.success) || _.isFunction(options.error) || _.isFunction(options.complete)) {
          console.warn('RB.DraftResourceModelMixin.destroy was ' + 'called using callbacks. Callers should be updated ' + 'to use promises instead.');
          return RB.promiseToCallbacks(options, context, newOptions => this.destroy(newOptions));
        }
        await this.ready();
        await _super(this).destroy.call(this, options);

        /* We need to fetch the draft resource again. */
        this._needDraft = true;
      },
      /**
       * Return the URL to use when syncing the model.
       *
       * Custom URL implementation which will return the special draft resource
       * if we have yet to redirect and otherwise delegate to the prototype
       * implementation.
       *
       * Returns:
       *     string:
       *     The URL to use for the resource.
       */
      url() {
        if (this._needDraft) {
          const parentObject = this.get('parentObject');
          const linkName = _.result(this, 'listKey');
          const links = parentObject.get('links');

          /*
           * Chrome hyper-aggressively caches things it shouldn't, and
           * appears to do so in a subtly broken way.
           *
           * If we do a DELETE on a reply's URL, then later a GET (resulting
           * from a redirect from a GET to draft/), Chrome will somehow get
           * confused and associate the GET's caching information with a 404.
           *
           * In order to prevent this, we need to make requests to draft/
           * appear unique. We can do this by appending the timestamp here.
           * Chrome will no longer end up with broken state for our later
           * GETs.
           *
           * Much of this is only required in the case of sqlite, which,
           * with Django, may reuse row IDs, causing problems when making
           * a reply, deleting, and making a new one. In production, this
           * shouldn't be a problem, but it's very confusing during
           * development.
           */
          return links[linkName].href + 'draft/?' + $.now();
        } else {
          return _super(this).url.call(this);
        }
      },
      /**
       * Try to retrieve an existing draft from the server.
       *
       * This uses the special draft/ resource within the resource list, which
       * will redirect to an existing draft if one exists.
       *
       * Args:
       *     options (object):
       *         Options for the operation, including callbacks.
       */
      _retrieveDraft(options) {
        if (!RB.UserSession.instance.get('authenticated')) {
          return Promise.reject(new BackboneError(this, {
            errorText: gettext("You must be logged in to retrieve the draft.")
          }, {}));
        }
        let data = options.data || {};
        const extraQueryArgs = _.result(this, 'extraQueryArgs', {});
        if (!_.isEmpty(extraQueryArgs)) {
          data = _.extend({}, extraQueryArgs, data);
        }
        return new Promise((resolve, reject) => {
          Backbone.Model.prototype.fetch.call(this, {
            data: data,
            error: (model, xhr, options) => {
              if (xhr.status === 404) {
                /*
                 * We now know we don't have an existing draft to work
                 * with, and will eventually need to POST to create a
                 * new one.
                 */
                this._needDraft = false;
                resolve();
              } else {
                reject(new BackboneError(model, xhr, options));
              }
            },
            processData: true,
            success: () => {
              /*
               * There was an existing draft, and we were redirected to
               * it and pulled data from it. We're done.
               */
              this._needDraft = false;
              resolve();
            }
          });
        });
      }
    };

    var _dec$3, _class$6;
    /**
     * A review reply.
     *
     * Encapsulates replies to a top-level review.
     */
    let ReviewReply = (_dec$3 = spina.spina({
      mixins: [DraftResourceModelMixin],
      prototypeAttrs: ['COMMENT_LINK_NAMES', 'attrToJsonMap', 'deserializedAttrs', 'extraQueryArgs', 'listKey', 'rspNamespace', 'serializedAttrs', 'serializers']
    }), _dec$3(_class$6 = class ReviewReply extends BaseResource {
      /**
       * Return default values for the model attributes.
       *
       * Returns:
       *     ReviewReplyAttrs:
       *     The default attributes.
       */
      defaults() {
        return _.defaults({
          bodyBottom: null,
          bodyBottomRichText: false,
          bodyTop: null,
          bodyTopRichText: false,
          forceTextType: null,
          includeTextTypes: null,
          'public': false,
          rawTextFields: {},
          review: null,
          timestamp: null
        }, super.defaults());
      }
      static rspNamespace = 'reply';
      static listKey = 'replies';
      static extraQueryArgs = {
        'force-text-type': 'html',
        'include-text-types': 'raw'
      };
      static attrToJsonMap = {
        bodyBottom: 'body_bottom',
        bodyBottomRichText: 'body_bottom_text_type',
        bodyTop: 'body_top',
        bodyTopRichText: 'body_top_text_type',
        forceTextType: 'force_text_type',
        includeTextTypes: 'include_text_types'
      };
      static serializedAttrs = ['bodyBottom', 'bodyBottomRichText', 'bodyTop', 'bodyTopRichText', 'forceTextType', 'includeTextTypes', 'public'];
      static deserializedAttrs = ['bodyBottom', 'bodyTop', 'public', 'timestamp'];
      static serializers = {
        bodyBottomRichText: textType,
        bodyTopRichText: textType,
        forceTextType: onlyIfValue,
        includeTextTypes: onlyIfValue,
        'public': value => {
          return value ? true : undefined;
        }
      };
      static COMMENT_LINK_NAMES = ['diff_comments', 'file_attachment_comments', 'general_comments', 'screenshot_comments'];

      /**
       * Parse the response from the server.
       *
       * Args:
       *     rsp (object):
       *         The response from the server.
       *
       * Returns:
       *     object:
       *     The attribute values to set on the model.
       */
      parseResourceData(rsp) {
        const rawTextFields = rsp.raw_text_fields || rsp;
        const data = super.parseResourceData(rsp);
        data.bodyTopRichText = rawTextFields.body_top_text_type === 'markdown';
        data.bodyBottomRichText = rawTextFields.body_bottom_text_type === 'markdown';
        data.rawTextFields = rsp.raw_text_fields || {};
        return data;
      }

      /**
       * Publish the reply.
       *
       * Before publishing, the "publishing" event will be triggered.
       * After successfully publishing, "published" will be triggered.
       *
       * Version Changed:
       *     5.0:
       *     Deprecated callbacks and added a promise return value.
       *
       * Args:
       *     options (object, optional):
       *         Options for the save operation.
       *
       *     context (object, optional):
       *         Context to bind when calling callbacks.
       *
       * Returns:
       *     Promise:
       *     A promise which resolves when the operation is complete.
       */
      async publish() {
        let options = arguments.length > 0 && arguments[0] !== undefined ? arguments[0] : {};
        let context = arguments.length > 1 && arguments[1] !== undefined ? arguments[1] : undefined;
        if (_.isFunction(options.success) || _.isFunction(options.error) || _.isFunction(options.complete)) {
          console.warn('RB.ReviewReply.publish was called using ' + 'callbacks. Callers should be updated to use ' + 'promises instead.');
          return RB.promiseToCallbacks(options, context, newOptions => this.publish(newOptions));
        }
        this.trigger('publishing');
        await this.ready();
        this.set('public', true);
        try {
          await this.save({
            data: {
              'public': 1,
              trivial: options.trivial ? 1 : 0
            }
          });
        } catch (err) {
          this.trigger('publishError', err.message);
          throw err;
        }
        this.trigger('published');
      }

      /**
       * Discard the reply if it's empty.
       *
       * If the reply doesn't have any remaining comments on the server, then
       * this will discard the reply.
       *
       * Version Changed:
       *     5.0:
       *     Changed to deprecate options and return a promise.
       *
       * Args:
       *     options (object, optional):
       *         Options for the save operation.
       *
       *     context (object, optional):
       *         Context to bind when calling callbacks.
       *
       * Returns:
       *     Promise:
       *     A promise which resolves when the operation is complete. The
       *     resolution value will be true if discarded, false otherwise.
       */
      async discardIfEmpty() {
        let options = arguments.length > 0 && arguments[0] !== undefined ? arguments[0] : {};
        let context = arguments.length > 1 && arguments[1] !== undefined ? arguments[1] : undefined;
        if (_.isFunction(options.success) || _.isFunction(options.error) || _.isFunction(options.complete)) {
          console.warn('RB.ReviewReply.discardIfEmpty was called using ' + 'callbacks. Callers should be updated to use ' + 'promises instead.');
          return RB.promiseToCallbacks(options, context, newOptions => this.discardIfEmpty(newOptions));
        }
        await this.ready();
        if (this.isNew() || this.get('bodyTop') || this.get('bodyBottom')) {
          return false;
        } else {
          return this._checkCommentsLink(0);
        }
      }

      /**
       * Check if there are comments, given the comment type.
       *
       * This is part of the discardIfEmpty logic.
       *
       * If there are comments, we'll give up and call options.success(false).
       *
       * If there are no comments, we'll move on to the next comment type. If
       * we're done, the reply is discarded, and options.success(true) is called.
       *
       * Args:
       *     linkNamesIndex (number):
       *         An index into the ``COMMENT_LINK_NAMES`` Array.
       *
       * Returns:
       *     Promise:
       *     A promise which resolves when the operation is complete. The
       *     resolution value will be true if discarded, false otherwise.
       */
      _checkCommentsLink(linkNameIndex) {
        return new Promise((resolve, reject) => {
          const linkName = ReviewReply.COMMENT_LINK_NAMES[linkNameIndex];
          const url = this.get('links')[linkName].href;
          RB.apiCall({
            error: (model, xhr, options) => reject(new BackboneError(model, xhr, options)),
            success: rsp => {
              if (rsp[linkName].length > 0) {
                resolve(false);
              } else if (linkNameIndex < ReviewReply.COMMENT_LINK_NAMES.length - 1) {
                resolve(this._checkCommentsLink(linkNameIndex + 1));
              } else {
                resolve(this.destroy().then(() => true));
              }
            },
            type: 'GET',
            url: url
          });
        });
      }
    }) || _class$6);

    var _dec$2, _class$5;

    /**
     * Attributes for the review model.
     *
     * Version Added:
     *     6.0
     */

    /**
     * A review.
     *
     * This corresponds to a top-level review. Replies are encapsulated in
     * ReviewReply.
     */
    let Review = (_dec$2 = spina.spina({
      prototypeAttrs: ['attrToJsonMap', 'deserializedAttrs', 'rspNamespace', 'serializedAttrs', 'serializers', 'supportsExtraData']
    }), _dec$2(_class$5 = class Review extends BaseResource {
      /**
       * Return default values for the model attributes.
       *
       * Returns:
       *     ReviewAttrs:
       *     The attribute defaults.
       */
      defaults() {
        return _.defaults({
          'authorName': null,
          'bodyBottom': null,
          'bodyBottomRichText': false,
          'bodyTop': null,
          'bodyTopRichText': false,
          'draftReply': null,
          'forceTextType': null,
          'htmlTextFields': {},
          'includeTextTypes': null,
          'markdownTextFields': {},
          'public': false,
          'rawTextFields': {},
          'shipIt': false,
          'timestamp': null
        }, super.defaults());
      }
      static rspNamespace = 'review';
      static attrToJsonMap = {
        bodyBottom: 'body_bottom',
        bodyBottomRichText: 'body_bottom_text_type',
        bodyTop: 'body_top',
        bodyTopRichText: 'body_top_text_type',
        forceTextType: 'force_text_type',
        includeTextTypes: 'include_text_types',
        shipIt: 'ship_it'
      };
      static serializedAttrs = ['forceTextType', 'includeTextTypes', 'shipIt', 'bodyTop', 'bodyTopRichText', 'bodyBottom', 'bodyBottomRichText', 'public'];
      static deserializedAttrs = ['shipIt', 'bodyTop', 'bodyBottom', 'public', 'timestamp'];
      static serializers = {
        'bodyBottomRichText': textType,
        'bodyTopRichText': textType,
        'forceTextType': onlyIfValue,
        'includeTextTypes': onlyIfValue,
        'public': value => {
          return value ? 1 : undefined;
        }
      };
      static supportsExtraData = true;

      /**
       * Parse the response from the server.
       *
       * Args:
       *    rsp (object):
       *        The response from the server.
       *
       * Returns:
       *     object:
       *     Attribute values to set on the model.
       */
      parseResourceData(rsp) {
        const rawTextFields = rsp.raw_text_fields || rsp;
        const data = super.parseResourceData(rsp);
        data.bodyTopRichText = rawTextFields.body_top_text_type === 'markdown';
        data.bodyBottomRichText = rawTextFields.body_bottom_text_type === 'markdown';
        if (rsp.raw_text_fields) {
          data.rawTextFields = {
            bodyBottom: rsp.raw_text_fields.body_bottom,
            bodyTop: rsp.raw_text_fields.body_top
          };
        }
        if (rsp.markdown_text_fields) {
          data.markdownTextFields = {
            bodyBottom: rsp.markdown_text_fields.body_bottom,
            bodyTop: rsp.markdown_text_fields.body_top
          };
        }
        if (rsp.html_text_fields) {
          data.htmlTextFields = {
            bodyBottom: rsp.html_text_fields.body_bottom,
            bodyTop: rsp.html_text_fields.body_top
          };
        }
        return data;
      }

      /**
       * Create a new diff comment for this review.
       *
       * Args:
       *     options (object):
       *         Options for creating the review.
       *
       * Option Args:
       *     id (number):
       *         The ID for the new model (in the case of existing comments).
       *
       *     fileDiffID (number):
       *         The ID of the FileDiff that this comment is for.
       *
       *     interFileDiffID (number):
       *         The ID of the FileDiff that represents the "new" side of an
       *         interdiff. If this is specified, the ``fileDiffID`` argument
       *         represents the "old" side.
       *
       *         This option is mutually exclusive with ``baseFileDiffID``.
       *
       *     beginLineNum (number):
       *         The line number of the start of the comment.
       *
       *     endLineNum (number):
       *         The line number of the end of the comment.
       *
       *     baseFileDiffID (number):
       *         The ID of the base FileDiff in the cumulative diff that the
       *         comment is to be made upon.
       *
       *         This option is mutually exclusive with ``interFileDiffID``.
       *
       * Returns:
       *     RB.DiffComment:
       *     The new comment object.
       */
      createDiffComment(options) {
        if (!!options.interFileDiffID && !!options.baseFileDiffID) {
          console.error('Options `interFileDiffID` and `baseFileDiffID` for ' + 'RB.Review.createDiffComment() are mutually exclusive.');
          return null;
        }
        return new RB.DiffComment(_.defaults({
          parentObject: this
        }, options));
      }

      /**
       * Create a new screenshot comment for this review.
       *
       * Args:
       *     id (number):
       *         The ID for the new model (in the case of existing comments).
       *
       *     screenshotID (number):
       *         The ID of the Screenshot that this comment is for.
       *
       *     x (number):
       *         The X coordinate of the pixel for the upper left of the comment
       *         region.
       *
       *     y (number):
       *         The Y coordinate of the pixel for the upper left of the comment
       *         region.
       *
       *     width (number):
       *         The width of the comment region, in pixels.
       *
       *     height (number):
       *         The height of the comment region, in pixels.
       *
       * Returns:
       *     RB.ScreenshotComment:
       *     The new comment object.
       */
      createScreenshotComment(id, screenshotID, x, y, width, height) {
        return new RB.ScreenshotComment({
          height: height,
          id: id,
          parentObject: this,
          screenshotID: screenshotID,
          width: width,
          x: x,
          y: y
        });
      }

      /**
       * Create a new file attachment comment for this review.
       *
       * Args:
       *     id (number):
       *         The ID for the new model (in the case of existing comments).
       *
       *     fileAttachmentID (number):
       *         The ID of the FileAttachment that this comment is for.
       *
       *     diffAgainstFileAttachmentID (number):
       *         The ID of the FileAttachment that the ``fileAttachmentID`` is
       *         diffed against, if the comment is for a file diff.
       *
       * Returns:
       *     RB.FileAttachmentComment:
       *     The new comment object.
       */
      createFileAttachmentComment(id, fileAttachmentID, diffAgainstFileAttachmentID) {
        return new RB.FileAttachmentComment({
          diffAgainstFileAttachmentID: diffAgainstFileAttachmentID,
          fileAttachmentID: fileAttachmentID,
          id: id,
          parentObject: this
        });
      }

      /**
       * Create a new general comment for this review.
       *
       * Args:
       *     id (number):
       *         The ID for the new model (in the case of existing comments).
       *
       *     issueOpened (boolean):
       *         Whether this comment should have an open issue.
       *
       * Returns:
       *     RB.GeneralComment:
       *     The new comment object.
       */
      createGeneralComment(id, issueOpened) {
        return new RB.GeneralComment({
          id: id,
          issueOpened: issueOpened,
          parentObject: this
        });
      }

      /**
       * Create a new reply.
       *
       * If an existing draft reply exists, return that. Otherwise create a draft
       * reply.
       *
       * Returns:
       *     RB.ReviewReply:
       *     The new reply object.
       */
      createReply() {
        let draftReply = this.get('draftReply');
        if (draftReply === null) {
          draftReply = new ReviewReply({
            parentObject: this
          });
          this.set('draftReply', draftReply);
          draftReply.once('published', () => {
            const reviewRequest = this.get('parentObject');
            reviewRequest.markUpdated(draftReply.get('timestamp'));
            this.set('draftReply', null);
          });
        }
        return draftReply;
      }
    }) || _class$5);

    var _dec$1, _class$4;

    /**
     * Attributes for the DraftReview model.
     *
     * Version Added:
     *     6.0
     */

    /**
     * A draft review.
     *
     * Draft reviews are more complicated than most objects. A draft may already
     * exist on the server, in which case we need to be able to get its ID. A
     * special resource exists at /reviews/draft/ which will redirect to the
     * existing draft if one exists, and return 404 if not.
     */
    let DraftReview = (_dec$1 = spina.spina({
      mixins: [DraftResourceModelMixin],
      prototypeAttrs: ['attrToJsonMap', 'serializedAttrs', 'serializers']
    }), _dec$1(_class$4 = class DraftReview extends Review {
      defaults() {
        return _.defaults({
          publishAndArchive: false,
          publishToOwnerOnly: false
        }, super.defaults());
      }
      static attrToJsonMap = _.defaults({
        publishAndArchive: 'publish_and_archive',
        publishToOwnerOnly: 'publish_to_owner_only'
      }, Review.attrToJsonMap);
      static serializedAttrs = ['publishAndArchive', 'publishToOwnerOnly'].concat(Review.serializedAttrs);
      static serializers = _.defaults({
        publishAndArchive: onlyIfValue,
        publishToOwnerOnly: onlyIfValue
      }, Review.serializers);

      /**
       * Publish the review.
       *
       * Before publish, the "publishing" event will be triggered.
       *
       * After the publish has succeeded, the "published" event will be
       * triggered.
       *
       * Version Changed:
       *     5.0:
       *     Deprecated the callbacks and added a promise return value.
       *
       * Args:
       *     options (object, optional):
       *         Options for the operation.
       *
       *     context (object, optional):
       *         Context to bind when calling callbacks.
       *
       * Returns:
       *     Promise:
       *     A promise which resolves when the operation is complete.
       */
      async publish() {
        let options = arguments.length > 0 && arguments[0] !== undefined ? arguments[0] : {};
        let context = arguments.length > 1 && arguments[1] !== undefined ? arguments[1] : undefined;
        if (_.isFunction(options.success) || _.isFunction(options.error) || _.isFunction(options.complete)) {
          console.warn(`RB.DraftReview.publish was called using callbacks.
                          Callers should be updated to use promises instead.`);
          return RB.promiseToCallbacks(options, context, newOptions => this.publish(newOptions));
        }
        this.trigger('publishing');
        await this.ready();
        this.set('public', true);
        try {
          await this.save({
            attrs: options.attrs
          });
        } catch (err) {
          this.trigger('publishError', err.xhr.errorText);
          throw err;
        }
        this.trigger('published');
      }
    }) || _class$4);

    var _class$3;

    /**
     * A message to send on the channel.
     *
     * Version Added:
     *     6.0.
     */

    /**
     * Communication channel to sync between tabs/windows.
     *
     * Version Added:
     *     6.0
     */
    let ClientCommChannel = spina.spina(_class$3 = class ClientCommChannel extends spina.BaseModel {
      static instance = null;

      /**
       * Return the ClientCommChannel instance.
       *
       * Returns:
       *     ClientCommChannel:
       *     The singleton instance.
       */
      static getInstance() {
        return this.instance;
      }

      /**********************
       * Instance variables *
       **********************/

      /** The broadcast channel instance. */
      #channel;

      /**
       * Initialize the model.
       */
      initialize() {
        console.assert(ClientCommChannel.instance === null);
        this.#channel = new BroadcastChannel('reviewboard');
        this.#channel.addEventListener('message', event => {
          const message = event.data;
          switch (message.event) {
            case 'reload':
              this._onReload(message);
              break;
            default:
              console.warn('Received unknown event from BroadcastChannel', message);
              break;
          }
        });
        ClientCommChannel.instance = this;
      }

      /**
       * Close the communication channel.
       */
      close() {
        this.#channel.close();
        console.assert(ClientCommChannel.instance === this);
        ClientCommChannel.instance = null;
      }

      /**
       * Send a reload signal to other tabs.
       */
      reload() {
        const page = RB.PageManager.getPage();
        const pageData = page.getReloadData();
        if (pageData === null) {
          console.warn(`Ignoring page reload request: No page data to send over the
broadcast channel. This would have affected all tabs without
reload data!`);
        } else {
          this.#channel.postMessage({
            data: pageData,
            event: 'reload'
          });
        }
      }

      /**
       * Handle a reload message from another tab.
       *
       * Args:
       *     message (Message):
       *         The message from the other tab.
       */
      _onReload(message) {
        const page = RB.PageManager.getPage();
        if (page) {
          const pageData = page.getReloadData();
          if (pageData !== null && _.isEqual(message.data, pageData)) {
            this.trigger('reload');
          }
        }
      }
    }) || _class$3;

    var _class$2;

    /**
     * Base class for page models.
     *
     * This doesn't provide any functionality by itself, but may be used in the
     * future for introducing additional logic for pages.
     *
     * This is intended for use by page views that are set by
     * :js:class:`RB.PageManager`.
     */
    let Page = spina.spina(_class$2 = class Page extends spina.BaseModel {}) || _class$2;

    var _dec, _class$1;
    /**
     * Base class for page views.
     *
     * This is responsible for setting up and handling the page's UI, including
     * the page header, mobile mode handling, and sidebars. It also provides some
     * utilities for setting up common UI elements.
     *
     * The page will respect the ``-has-sidebar`` and ``-is-content-full-page``
     * CSS classes on the document ``<body>``. These will control the behavior
     * and layout of the page.
     *
     * This is intended for use by page views that are set by
     * :js:class:`RB.PageManager`.
     */
    let PageView = (_dec = spina.spina({
      prototypeAttrs: ['windowResizeThrottleMS']
    }), _dec(_class$1 = class PageView extends spina.BaseView {
      /**
       * The maximum frequency at which resize events should be handled.
       *
       * Subclasses can override this if they need to respond to window
       * resizes at a faster or slower rate.
       */
      static windowResizeThrottleMS = 100;

      /**********************
       * Instance variables *
       **********************/

      /** The client (tab to tab) communication channel. */
      #commChannel = null;

      /** The sidebar element. */
      $mainSidebar = null;

      /** The page container element. */
      $pageContainer = null;

      /** The page content element. */
      $pageContent = null;

      /** The window, wrapped in JQuery. */

      /** The currently-shown pane for the sidebar. */
      _$mainSidebarPane = null;

      /** The page sidebar element */
      _$pageSidebar = null;

      /** The set of all panes in the sidebar. */
      _$pageSidebarPanes = null;

      /** A list of all registered action views. */
      _actionViews = [];

      /** The pop-out drawer, if the page has one. */
      drawer = null;

      /** Whether the page has a sidebar. */
      hasSidebar = null;

      /** The view for the page header. */
      headerView = null;

      /** Whether the page is currently in a mobile view. */
      inMobileMode = null;

      /** Whether the page is rendered in full-page content mode. */
      isFullPage = null;

      /**
       * Whether the page is rendered.
       *
       * Deprecated:
       *     6.0:
       *     Users should use :js:attr:`rendered` instead.
       */
      isPageRendered = false;
      /**
       * Initialize the page.
       *
       * Args:
       *     options (PageViewOptions, optional):
       *         Options for the page.
       */
      initialize() {
        let options = arguments.length > 0 && arguments[0] !== undefined ? arguments[0] : {};
        this.options = options;
        this.$window = $(window);
        if (!window.rbRunningTests) {
          this.#commChannel = new ClientCommChannel();
          this.listenTo(this.#commChannel, 'reload', () => {
            alert(gettext("This page is out of date and needs to be reloaded."));
            RB.reload();
          });
        }
      }

      /**
       * Remove the page from the DOM and disable event handling.
       *
       * Returns:
       *     PageView:
       *     This object, for chaining.
       */
      remove() {
        if (this.$window) {
          this.$window.off('resize.rbPageView');
        }
        if (this.headerView) {
          this.headerView.remove();
        }
        return super.remove();
      }

      /**
       * Render the page.
       *
       * Subclasses should not override this. Instead, they should override
       * :js:func:`RB.PageView.renderPage``.
       */
      onInitialRender() {
        const options = this.options;
        const $body = options.$body || $(document.body);
        this.$pageContainer = options.$pageContainer || $('#page-container');
        this.$pageContent = options.$pageContent || $('#content');
        this._$pageSidebar = options.$pageSidebar || $('#page-sidebar');
        this._$pageSidebarPanes = this._$pageSidebar.children('.rb-c-page-sidebar__panes');
        this._$mainSidebarPane = this._$pageSidebarPanes.children('.rb-c-page-sidebar__pane.-is-shown');
        this.$mainSidebar = this._$mainSidebarPane.children('.rb-c-page-sidebar__pane-content');
        this.headerView = new RB.HeaderView({
          $body: $body,
          $pageSidebar: this._$pageSidebar,
          el: options.$headerBar || $('#headerbar')
        });
        this.headerView.render();
        this.hasSidebar = $body.hasClass('-has-sidebar') || $body.hasClass('has-sidebar');
        this.isFullPage = $body.hasClass('-is-content-full-page') || $body.hasClass('full-page-content');
        this.inMobileMode = this.headerView.inMobileMode;
        this.renderPage();

        /*
         * Now that we've rendered the elements, we can show the page.
         */
        $body.addClass('-is-loaded');
        this.$window.on('resize.rbPageView', _.throttle(() => this._updateSize(), this.windowResizeThrottleMS));
        this.listenTo(this.headerView, 'mobileModeChanged', this._onMobileModeChanged);
        this._onMobileModeChanged(this.inMobileMode);
        this._actionViews.forEach(actionView => actionView.render());
        this.isPageRendered = true;
      }

      /**
       * Return data to use for assessing cross-tab page reloads.
       *
       * This is intended to be overridden by subclasses in order to filter which
       * reload signals apply to this page.
       *
       * Version Added:
       *     6.0
       */
      getReloadData() {
        return null;
      }

      /**
       * Set a drawer that can be shown over the sidebar.
       *
       * This is used by a page to set a drawer that should be displayed.
       * Drawers are shown over the sidebar area in desktop mode, or docked to
       * the bottom of the screen in mobile mode.
       *
       * Only one drawer can be set per page. Drawers also require a page with
       * sidebars enabled.
       *
       * Callers must instantiate the drawer but should not render it or
       * add it to the DOM.
       *
       * Args:
       *     drawer (RB.Drawer):
       *         The drawer to set.
       */
      setDrawer(drawer) {
        console.assert(this.drawer === null, 'A drawer has already been set up for this page.');
        console.assert(this.hasSidebar, 'Drawers can only be set up on pages with a sidebar.');
        this.drawer = drawer;
        drawer.render();
        this._reparentDrawer();
        this.listenTo(drawer, 'visibilityChanged', this._updateSize);
      }

      /**
       * Render the page contents.
       *
       * This should be implemented by subclasses that need to render any
       * UI elements.
       */
      renderPage() {
        // Do nothing.
      }

      /**
       * Resize an element to take the full height of a parent container.
       *
       * By default, this will size the element to the height of the main
       * page container. A specific parent can be specified for more specific
       * use cases.
       *
       * Args:
       *     $el (jQuery):
       *         The jQuery-wrapped element to resize.
       *
       *     $parent (jQuery, optional):
       *         The specific jQuery-wrapped parent element to base the size on.
       */
      resizeElementForFullHeight($el, $parent) {
        if ($parent === undefined) {
          $parent = this.$pageContainer;
        }
        $el.outerHeight($parent.height() - $el.position().top);
      }

      /**
       * Handle page resizes.
       *
       * This will be called whenever the page's size (or the window size)
       * has changed, allowing subclasses to adjust any UI elements as
       * appropriate.
       *
       * In the case of window sizes, calls to this function will be throttled,
       * called no more frequently than the configured
       * :js:attr:`windowResizeThrottleMS`.
       */
      onResize() {
        // Do nothing.
      }

      /**
       * Handle mobile mode changes.
       *
       * This will be called whenever the page goes between mobile/desktop
       * mode, allowing subclasses to adjust any UI elements as appropriate.
       *
       * Args:
       *     inMobileMode (boolean):
       *         Whether the UI is now in mobile mode. This will be the same
       *         value as :js:attr:`inMobileMode`, and is just provided for
       *         convenience.
       */
      onMobileModeChanged(inMobileMode) {
        // Do nothing.
      }

      /**
       * Add an action to the page.
       *
       * Args:
       *     actionView (RB.ActionView):
       *         The action instance.
       */
      addActionView(actionView) {
        this._actionViews.push(actionView);
        if (this.isPageRendered) {
          actionView.render();
        }
      }

      /**
       * Return the action view for the given action ID.
       *
       * Args:
       *     actionId (string):
       *         The ID of the action.
       *
       * Returns:
       *     RB.ActionView:
       *     The view for the given action.
       */
      getActionView(actionId) {
        for (const view of this._actionViews) {
          if (view.model.get('actionId') === actionId) {
            return view;
          }
        }
        return null;
      }

      /**
       * Update the size of the page.
       *
       * This will be called in response to window resizes and certain other
       * events. It will calculate the appropriate size for the sidebar (if
       * on the page) and the page container (if in full-page content mode),
       * update any elements as appropriate, and then call
       * :js:func:`RB.PageView.onResize` so that subclasses can update their
       * elements.
       */
      _updateSize() {
        const windowHeight = this.$window.height();
        let pageContainerHeight = null;
        let sidebarHeight = null;
        if (this.isFullPage) {
          pageContainerHeight = windowHeight - this.$pageContainer.offset().top;
        }
        if (this.inMobileMode) {
          if (pageContainerHeight !== null && this.drawer !== null && this.drawer.isVisible) {
            /*
             * If we're constraining the page container's height, and
             * there's a drawer present, reduce the page container's
             * height by the drawer size, so we don't make some content
             * inaccessible due to an overlap.
             */
            pageContainerHeight -= this.drawer.$el.outerHeight();
          }
        } else {
          if (pageContainerHeight !== null) {
            /*
             * If we're constraining the page container's height,
             * constrain the sidebar's as well.
             */
            sidebarHeight = windowHeight - this._$pageSidebar.offset().top;
          }
        }
        if (pageContainerHeight === null) {
          this.$pageContainer.css('height', '');
        } else {
          this.$pageContainer.outerHeight(pageContainerHeight);
        }
        if (sidebarHeight === null) {
          this._$pageSidebar.css('height', '');
        } else {
          this._$pageSidebar.outerHeight(sidebarHeight);
        }
        this.onResize();
      }

      /**
       * Set the new parent for the drawer.
       *
       * In mobile mode, this will place the drawer within the main
       * ``#container``, right before the sidebar, allowing it to appear docked
       * along the bottom of the page.
       *
       * In desktop mode, this will place the drawer within the sidebar area,
       * ensuring that it overlaps it properly.
       */
      _reparentDrawer() {
        const $el = this.drawer.$el.detach();
        if (this.inMobileMode) {
          $el.insertBefore(this._$pageSidebar);
        } else {
          $el.appendTo(this._$pageSidebarPanes);
        }
      }

      /**
       * Handle a transition between mobile and desktop mode.
       *
       * This will set the :js:attr:`inMobileMode` flag and trigger the
       * ``inMobileModeChanged`` event, so that pages can listen and update
       * their layout as appropriate.
       *
       * It will also update the size and reparent the drawer.
       *
       * Args:
       *     inMobileMode (boolean):
       *         Whether the page shell is in mobile mode.
       */
      _onMobileModeChanged(inMobileMode) {
        this.inMobileMode = inMobileMode;
        this._updateSize();
        if (this.drawer !== null) {
          this._reparentDrawer();
        }
        this.onMobileModeChanged(this.inMobileMode);
        this.trigger('inMobileModeChanged', this.inMobileMode);
      }
    }) || _class$1);

    var _class, _class2, _class3;
    /**
     * An item in a StoredItems list.
     *
     * These are used internally to proxy object registration into a store list.
     * It is meant to be a temporary, internal object that can be created with
     * the proper data and then immediately saved or deleted.
     *
     * Model Attributes:
     *     baseURL (string):
     *         The root of the URL for the resource list.
     *
     *     loaded (boolean):
     *         Whether the item is loaded from the server.
     *
     *     objectID (string):
     *         The ID of the item.
     *
     *     stored (boolean):
     *         Whether or not the item has been stored on the server.
     */
    let Item = spina.spina(_class = class Item extends BaseResource {
      /**
       * Return defaults for the model attributes.
       *
       * Returns:
       *     object:
       *     Default values for the attributes.
       */
      defaults() {
        return _.defaults({
          baseURL: null,
          loaded: true,
          objectID: null,
          stored: false
        }, super.defaults());
      }

      /**
       * Return the URL for the item resource.
       *
       * Returns:
       *     string:
       *     The URL to use for updating the item.
       */
      url() {
        let url = this.get('baseURL');
        if (this.get('stored')) {
          url += this.get('objectID') + '/';
        }
        return url;
      }

      /**
       * Return whether the item is new (not yet stored on the server).
       *
       * Returns:
       *     boolean:
       *     Whether the item is new.
       */
      isNew() {
        return !this.get('stored');
      }

      /**
       * Return a JSON-serializable representation of the item.
       *
       * Returns:
       *    object:
       *    A representation of the item suitable for serializing to JSON.
       */
      toJSON() {
        return {
          object_id: this.get('objectID') || undefined
        };
      }

      /**
       * Parse the response from the server.
       */
      parse( /* rsp */
      ) {
        return undefined;
      }
    }) || _class;
    /** Attributes for the StoredItems model. */
    /**
     * Manages a list of stored objects.
     *
     * This interfaces with a Watched Items resource (for groups or review
     * requests) and a Hidden Items resource, allowing immediate adding/removing
     * of objects.
     */
    let StoredItems = spina.spina(_class2 = class StoredItems extends BaseResource {
      /**
       * Return the defaults for the model attributes.
       *
       * Returns:
       *     object:
       *     The default values for the model attributes.
       */
      defaults() {
        return _.defaults({
          addError: '',
          removeError: ''
        }, super.defaults());
      }

      /**
       * Return the URL for the resource.
       *
       * Returns:
       *     string:
       *     The URL for the resource.
       */
      url() {
        return this.get('url');
      }

      /**
       * Immediately add an object to a stored list on the server.
       *
       * Version Changed:
       *     6.0:
       *     Removed options and context parameters.
       *
       * Version Changed:
       *     5.0:
       *     Deprecated the options and context parameters and changed to return
       *     a promise.
       *
       * Args:
       *     obj (Backbone.Model):
       *         The item to add.
       *
       *     options (object, optional):
       *         Options for the save operation.
       *
       *     context (object, optional):
       *         Context to use when calling the callbacks in ``options``.
       *
       * Returns:
       *     Promise:
       *     A promise which resolves when the operation is complete.
       */
      addImmediately(obj) {
        const url = this.url();
        if (url) {
          const item = new Item({
            baseURL: url,
            objectID: String(obj.id)
          });
          return item.save();
        } else {
          return Promise.reject(new Error(this.attributes.addError));
        }
      }

      /**
       * Immediately remove an object from a stored list on the server.
       *
       * Version Changed:
       *     6.0:
       *     Removed options and context parameters.
       *
       * Version Changed:
       *     5.0:
       *     Deprecated the options and context parameters and changed to return
       *     a promise.
       *
       * Args:
       *     obj (Backbone.Model):
       *         The item to remove.
       *
       * Returns:
       *     Promise:
       *     A promise which resolves when the operation is complete.
       */
      removeImmediately(obj) {
        const url = this.url();
        return new Promise((resolve, reject) => {
          if (url) {
            const item = new Item({
              baseURL: url,
              objectID: String(obj.id),
              stored: true
            });
            resolve(item.destroy());
          } else {
            reject(new Error(this.attributes.removeError));
          }
        });
      }
    }) || _class2;
    /** Attributes for the UserSession model. */
    /**
     * Manages the user's active session.
     *
     * This stores basic information on the user (the username and session API URL)
     * and utility objects such as the watched groups, watched review requests and
     * hidden review requests lists.
     *
     * There should only ever be one instance of a UserSession. It should always
     * be created through UserSession.create, and retrieved through
     * UserSession.instance.
     */
    let UserSession = spina.spina(_class3 = class UserSession extends spina.BaseModel {
      /** The singleton instance of the session object. */
      static instance = null;

      /**
       * Create the UserSession for the current user.
       *
       * Only one will ever exist. Calling this a second time will assert.
       *
       * Args:
       *     attributes (object):
       *         Attributes to pass into the UserSession initializer.
       *
       * Returns:
       *     UserSession:
       *     The user session instance.
       */
      static create(attributes) {
        console.assert(!this.instance, 'UserSession.create can only be called once.');
        this.instance = new this(attributes);
        return this.instance;
      }
      defaults = {
        archivedReviewRequestsURL: null,
        authenticated: false,
        diffsShowExtraWhitespace: false,
        fullName: null,
        loginURL: null,
        mutedReviewRequestsURL: null,
        readOnly: false,
        sessionURL: null,
        showReviewDialogTips: true,
        timezoneOffset: '0',
        userFileAttachmentsURL: null,
        userPageURL: null,
        username: null,
        watchedReviewGroupsURL: null,
        watchedReviewRequestsURL: null
      };

      /**********************
       * Instance variables *
       **********************/

      /** The API endpoint for archiving. */

      /**
       * Initialize the model.
       */
      initialize() {
        this.watchedGroups = new StoredItems({
          url: this.get('watchedReviewGroupsURL'),
          addError: gettext("Must log in to add a watched item."),
          removeError: gettext("Must log in to remove a watched item.")
        });
        this.watchedReviewRequests = new StoredItems({
          url: this.get('watchedReviewRequestsURL'),
          addError: gettext("Must log in to add a watched item."),
          removeError: gettext("Must log in to remove a watched item.")
        });
        this.archivedReviewRequests = new StoredItems({
          url: this.get('archivedReviewRequestsURL'),
          removeError: gettext("Must log in to remove a archived item."),
          addError: gettext("Must log in to add an archived item.")
        });
        this.mutedReviewRequests = new StoredItems({
          url: this.get('mutedReviewRequestsURL'),
          removeError: gettext("Must log in to remove a muted item."),
          addError: gettext("Must log in to add a muted item.")
        });
        this._bindCookie({
          attr: 'diffsShowExtraWhitespace',
          cookieName: 'show_ew',
          deserialize: value => value !== 'false'
        });
        this._bindCookie({
          attr: 'showReviewDialogTips',
          cookieName: 'show_review_dialog_tips',
          deserialize: value => value !== 'false'
        });
      }

      /**
       * Toggle a boolean attribute.
       *
       * The attribute will be the inverse of the prior value.
       *
       * Args:
       *     attr (string):
       *         The name of the attribute to toggle.
       */
      toggleAttr(attr) {
        this.set(attr, !this.get(attr));
      }

      /*
       * Return avatar HTML for the user with the given size.
       *
       * Version Added:
       *     3.0.19
       *
       * Args:
       *     size (Number):
       *         The size of the avatar, in pixels. This is both the width and
       *         height.
       *
       * Return:
       *     string:
       *     The HTML for the avatar.
       */
      getAvatarHTML(size) {
        const urls = this.get('avatarHTML') || {};
        return urls[size] || '';
      }

      /**
       * Bind a cookie to an attribute.
       *
       * The initial value of the attribute will be set to that of the cookie.
       *
       * When the attribute changes, the cookie will be updated.
       *
       * Args:
       *     options (object):
       *         Options for the bind.
       *
       * Option Args:
       *    attr (string):
       *        The name of the attribute to bind.
       *
       *    cookieName (string):
       *        The name of the cookie to store.
       *
       *    deserialize (function, optional):
       *        A deserialization function to use when fetching the attribute
       *        value.
       *
       *    serialize (function, optional):
       *        A serialization function to use when storing the attribute value.
       */
      _bindCookie(options) {
        const deserialize = options.deserialize || _.identity;
        const serialize = options.serialize || (value => value.toString());
        this.set(options.attr, deserialize($.cookie(options.cookieName)));
        this.on(`change:${options.attr}`, (model, value) => {
          $.cookie(options.cookieName, serialize(value), {
            path: SITE_ROOT
          });
        });
      }
    }) || _class3;

    /**
     * Library for the base-level state and functionality for Review Board.
     *
     * Version Added:
     *     6.0
     */

    /**
     * An interface defining the structure of enabled feature maps.
     *
     * Version Added:
     *     6.0
     */

    /**
     * An interface defining the product information for Review Board.
     *
     * Version Added:
     *     6.0
     */

    /**
     * A mapping of enabled features.
     *
     * Each key corresponds to a feature ID, and each value is set to ``true``.
     *
     * This is filled in on page load. It's empty by default.
     *
     * Version Added:
     *     3.0
     */
    const EnabledFeatures = {};

    /**
     * Information on the running version of Review Board.
     *
     * This is filled in on page load. It's set to mostly blank values by default.
     *
     * Version Added:
     *     4.0
     */
    const Product = {
      isRelease: false,
      manualURL: '',
      name: 'Review Board',
      version: '',
      versionInfo: [0, 0, 0, 0, '', 0]
    };

    exports.Actions = Actions;
    exports.BaseCollection = BaseCollection;
    exports.BaseResource = BaseResource;
    exports.ClientCommChannel = ClientCommChannel;
    exports.DraftFileAttachment = DraftFileAttachment;
    exports.DraftResourceChildModelMixin = DraftResourceChildModelMixin;
    exports.DraftResourceModelMixin = DraftResourceModelMixin;
    exports.DraftReview = DraftReview;
    exports.EnabledFeatures = EnabledFeatures;
    exports.ExtraData = ExtraData;
    exports.ExtraDataMixin = ExtraDataMixin;
    exports.FileAttachment = FileAttachment;
    exports.JSONSerializers = serializers;
    exports.Page = Page;
    exports.PageView = PageView;
    exports.Product = Product;
    exports.ResourceCollection = ResourceCollection;
    exports.Review = Review;
    exports.ReviewReply = ReviewReply;
    exports.UserSession = UserSession;

    Object.defineProperty(exports, Symbol.toStringTag, { value: 'Module' });

}));
//# sourceMappingURL=index.js.map
