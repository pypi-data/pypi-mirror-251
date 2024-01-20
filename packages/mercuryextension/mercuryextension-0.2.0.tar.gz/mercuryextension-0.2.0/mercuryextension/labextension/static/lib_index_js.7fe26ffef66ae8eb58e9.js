"use strict";
(self["webpackChunk_mljar_mercuryextension"] = self["webpackChunk_mljar_mercuryextension"] || []).push([["lib_index_js"],{

/***/ "./lib/commands/index.js":
/*!*******************************!*\
  !*** ./lib/commands/index.js ***!
  \*******************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   commands: () => (/* binding */ commands)
/* harmony export */ });
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/notebook */ "webpack/sharing/consume/default/@jupyterlab/notebook");
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0__);

function runAllBelow(notebook, sessionContext, sessionDialogs, translator) {
    if (!notebook.model || !notebook.activeCell) {
        return Promise.resolve(false);
    }
    const cellIndex = notebook.activeCellIndex;
    notebook.activeCellIndex = notebook.activeCellIndex + 1;
    const promise = _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0__.NotebookActions.runAllBelow(notebook, sessionContext, sessionDialogs, translator);
    promise.finally(() => {
        notebook.activeCellIndex = cellIndex;
    });
}
const commands = {
    id: '@mljar/mercury-commands',
    description: 'Commands used in Mercury',
    autoStart: true,
    requires: [_jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0__.INotebookTracker],
    activate: (app, notebookTracker) => {
        const commandID = '@mljar/mercury-execute-below';
        app.commands.addCommand(commandID, {
            label: 'Execute cells below',
            execute: () => {
                const nb = notebookTracker.currentWidget;
                if (nb) {
                    console.log('Run all below');
                    runAllBelow(nb.content, nb.context.sessionContext);
                }
            }
        });
    }
};


/***/ }),

/***/ "./lib/icons.js":
/*!**********************!*\
  !*** ./lib/icons.js ***!
  \**********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   partyIcon: () => (/* binding */ partyIcon)
/* harmony export */ });
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _style_icons_party_svg__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../style/icons/party.svg */ "./style/icons/party.svg");

// icon svg import statements

const partyIcon = new _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__.LabIcon({
    name: '@mljar/party-icon',
    svgstr: _style_icons_party_svg__WEBPACK_IMPORTED_MODULE_1__
});


/***/ }),

/***/ "./lib/index.js":
/*!**********************!*\
  !*** ./lib/index.js ***!
  \**********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _mercury__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./mercury */ "./lib/mercury/index.js");
/* harmony import */ var _widgets__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./widgets */ "./lib/widgets/index.js");
/* harmony import */ var _commands__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./commands */ "./lib/commands/index.js");



const plugins = [_mercury__WEBPACK_IMPORTED_MODULE_0__.mercury, _widgets__WEBPACK_IMPORTED_MODULE_1__.widgets, _commands__WEBPACK_IMPORTED_MODULE_2__.commands];
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (plugins);


/***/ }),

/***/ "./lib/mercury/app/item/model.js":
/*!***************************************!*\
  !*** ./lib/mercury/app/item/model.js ***!
  \***************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   CellItemModel: () => (/* binding */ CellItemModel)
/* harmony export */ });
/* harmony import */ var _lumino_signaling__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @lumino/signaling */ "webpack/sharing/consume/default/@lumino/signaling");
/* harmony import */ var _lumino_signaling__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_lumino_signaling__WEBPACK_IMPORTED_MODULE_0__);

class CellItemModel {
    constructor(options) {
        this._cellId = '';
        // place cell in the sidebar or not
        this._sidebar = false;
        this._cellId = options.cellId;
        this._sidebar = options.sidebar;
    }
    get cellId() {
        return this._cellId;
    }
    get sidebar() {
        return this._sidebar;
    }
    dispose() {
        _lumino_signaling__WEBPACK_IMPORTED_MODULE_0__.Signal.clearData(this);
    }
}


/***/ }),

/***/ "./lib/mercury/app/item/widget.js":
/*!****************************************!*\
  !*** ./lib/mercury/app/item/widget.js ***!
  \****************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   CellItemWidget: () => (/* binding */ CellItemWidget)
/* harmony export */ });
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @lumino/widgets */ "webpack/sharing/consume/default/@lumino/widgets");
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_lumino_widgets__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _model__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./model */ "./lib/mercury/app/item/model.js");


class CellItemWidget extends _lumino_widgets__WEBPACK_IMPORTED_MODULE_0__.Panel {
    constructor(cell, options) {
        super();
        this.removeClass('lm-Widget');
        this.removeClass('p-Widget');
        this.addClass('cell-item-widget');
        this._model = new _model__WEBPACK_IMPORTED_MODULE_1__.CellItemModel(options);
        const content = new _lumino_widgets__WEBPACK_IMPORTED_MODULE_0__.Panel();
        content.addClass('cell-item-content');
        cell.addClass('cell-item-widget');
        content.addWidget(cell);
        this.addWidget(content);
    }
    dispose() {
        if (this.isDisposed) {
            return;
        }
        this._model.dispose();
        super.dispose();
    }
    get cellId() {
        return this._model.cellId;
    }
    get sidebar() {
        return this._model.sidebar;
    }
}


/***/ }),

/***/ "./lib/mercury/app/model.js":
/*!**********************************!*\
  !*** ./lib/mercury/app/model.js ***!
  \**********************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   AppModel: () => (/* binding */ AppModel)
/* harmony export */ });
/* harmony import */ var _jupyterlab_cells__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/cells */ "webpack/sharing/consume/default/@jupyterlab/cells");
/* harmony import */ var _jupyterlab_cells__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_cells__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_outputarea__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/outputarea */ "webpack/sharing/consume/default/@jupyterlab/outputarea");
/* harmony import */ var _jupyterlab_outputarea__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_outputarea__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyter_ydoc__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyter/ydoc */ "webpack/sharing/consume/default/@jupyter/ydoc");
/* harmony import */ var _jupyter_ydoc__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyter_ydoc__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _lumino_signaling__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @lumino/signaling */ "webpack/sharing/consume/default/@lumino/signaling");
/* harmony import */ var _lumino_signaling__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_lumino_signaling__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var yjs__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! yjs */ "webpack/sharing/consume/default/yjs");
/* harmony import */ var yjs__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(yjs__WEBPACK_IMPORTED_MODULE_4__);
/* harmony import */ var _item_widget__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ./item/widget */ "./lib/mercury/app/item/widget.js");






class AppModel {
    constructor(options) {
        this._mutex = (0,_jupyter_ydoc__WEBPACK_IMPORTED_MODULE_2__.createMutex)();
        this._ystate = new yjs__WEBPACK_IMPORTED_MODULE_4__.Map();
        this._context = options.context;
        this.rendermime = options.rendermime;
        this.contentFactory = options.contentFactory;
        this.mimeTypeService = options.mimeTypeService;
        this._editorConfig = options.editorConfig;
        this._notebookConfig = options.notebookConfig;
        this._ready = new _lumino_signaling__WEBPACK_IMPORTED_MODULE_3__.Signal(this);
        this._cellRemoved = new _lumino_signaling__WEBPACK_IMPORTED_MODULE_3__.Signal(this);
        this._stateChanged = new _lumino_signaling__WEBPACK_IMPORTED_MODULE_3__.Signal(this);
        this._contentChanged = new _lumino_signaling__WEBPACK_IMPORTED_MODULE_3__.Signal(this);
        this._context.sessionContext.ready.then(() => {
            const ymodel = this._context.model.sharedModel;
            this._ystate = ymodel.ystate;
            if (this._ystate.get('executed') !== true) {
                ymodel.transact(() => {
                    this._ystate.set('executed', false);
                }, false);
            }
            this._context.save().then(v => {
                this._ready.emit(null);
            });
        });
        this._context.model.contentChanged.connect(this._updateCells, this);
    }
    /**
     * A signal emitted when the model is ready.
     */
    get ready() {
        return this._ready;
    }
    /**
     * A signal emitted when a cell is removed.
     */
    get cellRemoved() {
        return this._cellRemoved;
    }
    /**
     * A signal emitted when the model state changes.
     */
    get stateChanged() {
        return this._stateChanged;
    }
    /**
     * A signal emitted when the model content changes.
     */
    get contentChanged() {
        return this._contentChanged;
    }
    /**
     * A config object for cell editors.
     */
    get editorConfig() {
        return this._editorConfig;
    }
    /**
     * A config object for cell editors.
     *
     * @param value - A `StaticNotebook.IEditorConfig`.
     */
    set editorConfig(value) {
        this._editorConfig = value;
    }
    /**
     * A config object for notebook widget.
     */
    get notebookConfig() {
        return this._notebookConfig;
    }
    /**
     * A config object for notebook widget.
     *
     * @param value - A `StaticNotebook.INotebookConfig`.
     */
    set notebookConfig(value) {
        this._notebookConfig = value;
    }
    set executed(value) {
        this._ystate.set('executed', value);
    }
    /**
     * The Notebook's cells.
     */
    get cells() {
        return this._context.model.cells;
    }
    /**
     * Ids of the notebooks's deleted cells.
     */
    get deletedCells() {
        return this._context.model.deletedCells;
    }
    /**
     * Create a new cell widget from a `CellModel`.
     *
     * @param cellModel - `ICellModel`.
     */
    createCell(cellModel, hideOutput = false) {
        let item;
        let sidebar = false;
        switch (cellModel.type) {
            case 'code': {
                const codeCell = new _jupyterlab_cells__WEBPACK_IMPORTED_MODULE_0__.CodeCell({
                    model: cellModel,
                    rendermime: this.rendermime,
                    contentFactory: this.contentFactory,
                    editorConfig: this._editorConfig.code
                });
                codeCell.readOnly = true;
                for (let i = 0; i < codeCell.outputArea.model.length; i++) {
                    const output = codeCell.outputArea.model.get(i);
                    const data = output.data;
                    if ('application/vnd.jupyter.widget-view+json' in data) {
                        sidebar = true;
                    }
                }
                if (sidebar && !hideOutput) {
                    item = new _jupyterlab_outputarea__WEBPACK_IMPORTED_MODULE_1__.SimplifiedOutputArea({
                        model: codeCell.outputArea.model,
                        rendermime: codeCell.outputArea.rendermime,
                        contentFactory: codeCell.outputArea.contentFactory
                    });
                }
                else {
                    item = codeCell;
                    if (hideOutput) {
                        const opts = {
                            config: this._editorConfig.code
                        };
                        //codeCell.inputArea
                        //  ?.contentFactory as InputArea.IContentFactory, // this.contentFactory,
                        item = new _jupyterlab_cells__WEBPACK_IMPORTED_MODULE_0__.InputArea({
                            model: cellModel,
                            contentFactory: this.contentFactory,
                            editorOptions: opts
                        });
                    }
                }
                break;
            }
            case 'markdown': {
                const markdownCell = new _jupyterlab_cells__WEBPACK_IMPORTED_MODULE_0__.MarkdownCell({
                    model: cellModel,
                    rendermime: this.rendermime,
                    contentFactory: this.contentFactory,
                    editorConfig: this._editorConfig.markdown
                });
                markdownCell.inputHidden = false;
                markdownCell.rendered = true;
                Private.removeElements(markdownCell.node, 'jp-Collapser');
                Private.removeElements(markdownCell.node, 'jp-InputPrompt');
                item = markdownCell;
                break;
            }
            default: {
                const rawCell = new _jupyterlab_cells__WEBPACK_IMPORTED_MODULE_0__.RawCell({
                    model: cellModel,
                    contentFactory: this.contentFactory,
                    editorConfig: this._editorConfig.raw
                });
                rawCell.inputHidden = false;
                Private.removeElements(rawCell.node, 'jp-Collapser');
                Private.removeElements(rawCell.node, 'jp-InputPrompt');
                item = rawCell;
                break;
            }
        }
        const options = {
            cellId: cellModel.id,
            cellWidget: item,
            sidebar
        };
        const widget = new _item_widget__WEBPACK_IMPORTED_MODULE_5__.CellItemWidget(item, options);
        return widget;
    }
    /**
     * Execute a CodeCell.
     *
     * @param cell - `ICellModel`.
     */
    execute(cell) {
        if (cell.type !== 'code' || this._ystate.get('executed')) {
            return;
        }
        const codeCell = new _jupyterlab_cells__WEBPACK_IMPORTED_MODULE_0__.CodeCell({
            model: cell,
            rendermime: this.rendermime,
            contentFactory: this.contentFactory,
            editorConfig: this._editorConfig.code
        });
        _jupyterlab_outputarea__WEBPACK_IMPORTED_MODULE_1__.SimplifiedOutputArea.execute(cell.sharedModel.source, codeCell.outputArea, this._context.sessionContext)
            .then(resp => {
            if ((resp === null || resp === void 0 ? void 0 : resp.header.msg_type) === 'execute_reply' &&
                resp.content.status === 'ok') {
                cell.executionCount = resp.content.execution_count;
            }
        })
            .catch(reason => console.error(reason));
    }
    /**
     * Update cells.
     */
    _updateCells() {
        this._mutex(() => {
            this._contentChanged.emit(null);
            console.log('content changed');
        });
    }
}
/**
 * A namespace for private module data.
 */
var Private;
(function (Private) {
    /**
     * Remove children by className from an HTMLElement.
     */
    function removeElements(node, className) {
        const elements = node.getElementsByClassName(className);
        for (let i = 0; i < elements.length; i++) {
            elements[i].remove();
        }
    }
    Private.removeElements = removeElements;
})(Private || (Private = {}));


/***/ }),

/***/ "./lib/mercury/app/widget.js":
/*!***********************************!*\
  !*** ./lib/mercury/app/widget.js ***!
  \***********************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   AppWidget: () => (/* binding */ AppWidget)
/* harmony export */ });
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @lumino/widgets */ "webpack/sharing/consume/default/@lumino/widgets");
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_lumino_widgets__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _lumino_signaling__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @lumino/signaling */ "webpack/sharing/consume/default/@lumino/signaling");
/* harmony import */ var _lumino_signaling__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_lumino_signaling__WEBPACK_IMPORTED_MODULE_1__);


class AppWidget extends _lumino_widgets__WEBPACK_IMPORTED_MODULE_0__.Panel {
    constructor(model) {
        super();
        this._cellItems = [];
        this.id = 'mercury-main-panel';
        this.addClass('mercury-main-panel');
        this._model = model;
        this._model.ready.connect(() => {
            this._initCellItems();
        });
        this._left = new _lumino_widgets__WEBPACK_IMPORTED_MODULE_0__.Panel();
        this._right = new _lumino_widgets__WEBPACK_IMPORTED_MODULE_0__.Panel();
        this._left.addClass('mercury-left-panel');
        this._right.addClass('mercury-right-panel');
        this.addWidget(this._left);
        this.addWidget(this._right);
    }
    _initCellItems() {
        const cells = this._model.cells;
        for (let i = 0; i < (cells === null || cells === void 0 ? void 0 : cells.length); i++) {
            const model = cells.get(i);
            const item = this._model.createCell(model);
            this._cellItems.push(item);
            if (item.sidebar) {
                this._left.addWidget(item);
                const item_only_input = this._model.createCell(model, true);
                this._right.addWidget(item_only_input);
                this._cellItems.push(item_only_input);
            }
            else {
                this._right.addWidget(item);
            }
        }
    }
    /**
     * Dispose of the resources held by the widget.
     */
    dispose() {
        if (this.isDisposed) {
            return;
        }
        _lumino_signaling__WEBPACK_IMPORTED_MODULE_1__.Signal.clearData(this);
        super.dispose();
    }
    /**
     * Handle `after-attach` messages sent to the widget.
     *
     * ### Note
     * Add event listeners for the drag and drop event.
     */
    onAfterAttach(msg) {
        super.onAfterAttach(msg);
    }
    /**
     * Handle `before-detach` messages sent to the widget.
     *
     * ### Note
     * Remove event listeners for the drag and drop event.
     */
    onBeforeDetach(msg) {
        super.onBeforeDetach(msg);
    }
    get cellWidgets() {
        return this._cellItems;
    }
    executeCellItems() {
        const cells = this._model.cells;
        this._model.executed = false;
        for (let i = 0; i < (cells === null || cells === void 0 ? void 0 : cells.length); i++) {
            const model = cells.get(i);
            this._model.execute(model);
        }
        this._model.executed = true;
    }
}


/***/ }),

/***/ "./lib/mercury/factory.js":
/*!********************************!*\
  !*** ./lib/mercury/factory.js ***!
  \********************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   MercuryWidgetFactory: () => (/* binding */ MercuryWidgetFactory)
/* harmony export */ });
/* harmony import */ var _jupyterlab_docregistry__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/docregistry */ "webpack/sharing/consume/default/@jupyterlab/docregistry");
/* harmony import */ var _jupyterlab_docregistry__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_docregistry__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/notebook */ "webpack/sharing/consume/default/@jupyterlab/notebook");
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _widget__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./widget */ "./lib/mercury/widget.js");
/* harmony import */ var _panel__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./panel */ "./lib/mercury/panel.js");




class MercuryWidgetFactory extends _jupyterlab_docregistry__WEBPACK_IMPORTED_MODULE_0__.ABCWidgetFactory {
    constructor(options) {
        super(options);
        this.rendermime = options.rendermime;
        this.contentFactory =
            options.contentFactory ||
                new _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_1__.NotebookPanel.ContentFactory({
                    editorFactory: options.editorFactoryService.newInlineEditor
                });
        this.mimeTypeService = options.mimeTypeService;
        this._editorConfig =
            options.editorConfig || _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_1__.StaticNotebook.defaultEditorConfig;
        this._notebookConfig =
            options.notebookConfig || _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_1__.StaticNotebook.defaultNotebookConfig;
    }
    /**
     * A configuration object for cell editor settings.
     */
    get editorConfig() {
        return this._editorConfig;
    }
    set editorConfig(value) {
        this._editorConfig = value;
    }
    /**
     * A configuration object for notebook settings.
     */
    get notebookConfig() {
        return this._notebookConfig;
    }
    set notebookConfig(value) {
        this._notebookConfig = value;
    }
    createNewWidget(context, source) {
        const options = {
            context: context,
            rendermime: source
                ? source.content.rendermime
                : this.rendermime.clone({ resolver: context.urlResolver }),
            contentFactory: this.contentFactory,
            mimeTypeService: this.mimeTypeService,
            editorConfig: source ? source.content.editorConfig : this._editorConfig,
            notebookConfig: source
                ? source.content.notebookConfig
                : this._notebookConfig
        };
        return new _widget__WEBPACK_IMPORTED_MODULE_2__.MercuryWidget(context, new _panel__WEBPACK_IMPORTED_MODULE_3__.MercuryPanel(options));
    }
}


/***/ }),

/***/ "./lib/mercury/index.js":
/*!******************************!*\
  !*** ./lib/mercury/index.js ***!
  \******************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   mercury: () => (/* binding */ mercury)
/* harmony export */ });
/* harmony import */ var _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/application */ "webpack/sharing/consume/default/@jupyterlab/application");
/* harmony import */ var _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/notebook */ "webpack/sharing/consume/default/@jupyterlab/notebook");
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/rendermime */ "webpack/sharing/consume/default/@jupyterlab/rendermime");
/* harmony import */ var _jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _jupyterlab_codeeditor__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @jupyterlab/codeeditor */ "webpack/sharing/consume/default/@jupyterlab/codeeditor");
/* harmony import */ var _jupyterlab_codeeditor__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_codeeditor__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_4__);
/* harmony import */ var _jupyterlab_mainmenu__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @jupyterlab/mainmenu */ "webpack/sharing/consume/default/@jupyterlab/mainmenu");
/* harmony import */ var _jupyterlab_mainmenu__WEBPACK_IMPORTED_MODULE_5___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_mainmenu__WEBPACK_IMPORTED_MODULE_5__);
/* harmony import */ var _factory__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ./factory */ "./lib/mercury/factory.js");
/* harmony import */ var _widget__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ./widget */ "./lib/mercury/widget.js");
/* harmony import */ var _toolbar_button__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! ./toolbar/button */ "./lib/mercury/toolbar/button.js");









const mercury = {
    id: '@mljar:mercury-extension',
    autoStart: true,
    provides: _widget__WEBPACK_IMPORTED_MODULE_6__.IMercuryTracker,
    requires: [
        _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_1__.NotebookPanel.IContentFactory,
        _jupyterlab_mainmenu__WEBPACK_IMPORTED_MODULE_5__.IMainMenu,
        _jupyterlab_codeeditor__WEBPACK_IMPORTED_MODULE_3__.IEditorServices,
        _jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_2__.IRenderMimeRegistry
    ],
    optional: [_jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.ILayoutRestorer],
    activate: (app, contentFactory, mainMenu, editorServices, rendermime) => {
        console.log('Mercury extension is active.');
        const tracker = new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_4__.WidgetTracker({
            namespace: '@mljar/mercury-widget-tracker'
        });
        const factory = new _factory__WEBPACK_IMPORTED_MODULE_7__.MercuryWidgetFactory({
            name: 'Mercury',
            fileTypes: ['notebook'],
            modelName: 'notebook',
            preferKernel: true,
            canStartKernel: true,
            rendermime: rendermime,
            contentFactory,
            editorConfig: _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_1__.StaticNotebook.defaultEditorConfig,
            notebookConfig: _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_1__.StaticNotebook.defaultNotebookConfig,
            mimeTypeService: editorServices.mimeTypeService,
            editorFactoryService: editorServices.factoryService,
            notebookPanel: null
        });
        factory.widgetCreated.connect((sender, widget) => {
            widget.context.pathChanged.connect(() => {
                void tracker.save(widget);
            });
            void tracker.add(widget);
            widget.update();
            app.commands.notifyCommandChanged();
        });
        app.docRegistry.addWidgetFactory(factory);
        app.docRegistry.addWidgetExtension('Notebook', new _toolbar_button__WEBPACK_IMPORTED_MODULE_8__.OpenMercuryButton(app.commands));
        return tracker;
    }
};


/***/ }),

/***/ "./lib/mercury/panel.js":
/*!******************************!*\
  !*** ./lib/mercury/panel.js ***!
  \******************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   MercuryPanel: () => (/* binding */ MercuryPanel)
/* harmony export */ });
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @lumino/widgets */ "webpack/sharing/consume/default/@lumino/widgets");
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_lumino_widgets__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _lumino_signaling__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @lumino/signaling */ "webpack/sharing/consume/default/@lumino/signaling");
/* harmony import */ var _lumino_signaling__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_lumino_signaling__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _app_model__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./app/model */ "./lib/mercury/app/model.js");
/* harmony import */ var _app_widget__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./app/widget */ "./lib/mercury/app/widget.js");




class MercuryPanel extends _lumino_widgets__WEBPACK_IMPORTED_MODULE_0__.Panel {
    constructor(options) {
        super();
        this.addClass('jp-Notebook');
        this.addClass('jp-NotebookPanel-notebook');
        this.addClass('mercury-panel');
        this._context = options.context;
        this.rendermime = options.rendermime;
        this.contentFactory = options.contentFactory;
        this.mimeTypeService = options.mimeTypeService;
        this._editorConfig = options.editorConfig;
        this._notebookConfig = options.notebookConfig;
        const appModel = new _app_model__WEBPACK_IMPORTED_MODULE_2__.AppModel({
            context: this._context,
            rendermime: this.rendermime,
            contentFactory: this.contentFactory,
            mimeTypeService: this.mimeTypeService,
            editorConfig: this._editorConfig,
            notebookConfig: this._notebookConfig
        });
        this._appWidget = new _app_widget__WEBPACK_IMPORTED_MODULE_3__.AppWidget(appModel);
        this.addWidget(this._appWidget);
    }
    /**
     * Dispose of the resources held by the widget.
     */
    dispose() {
        _lumino_signaling__WEBPACK_IMPORTED_MODULE_1__.Signal.clearData(this);
        super.dispose();
    }
    /**
     * Getter for the notebook cell editor configuration.
     */
    get editorConfig() {
        return this._editorConfig;
    }
    /**
     * Setter for the notebook cell editor configuration.
     *
     * @param value - The `EditorConfig` of the notebook.
     */
    set editorConfig(value) {
        this._editorConfig = value;
    }
    get notebookConfig() {
        return this._notebookConfig;
    }
    set notebookConfig(value) {
        this._notebookConfig = value;
    }
    get cellWidgets() {
        return this._appWidget.cellWidgets;
    }
}


/***/ }),

/***/ "./lib/mercury/toolbar/button.js":
/*!***************************************!*\
  !*** ./lib/mercury/toolbar/button.js ***!
  \***************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   OpenMercuryButton: () => (/* binding */ OpenMercuryButton)
/* harmony export */ });
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @lumino/widgets */ "webpack/sharing/consume/default/@lumino/widgets");
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_lumino_widgets__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _icons__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../../icons */ "./lib/icons.js");



/**
 * A WidgetExtension for Notebook's toolbar to open a `Mercury` widget.
 */
class OpenMercuryButton {
    /**
     * Instantiate a new NotebookButton.
     * @param commands The command registry.
     */
    constructor(commands) {
        this._commands = commands;
    }
    /**
     * Create a new extension object.
     */
    createNew(panel) {
        const button = new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.ToolbarButton({
            tooltip: 'Open with Mercury',
            icon: _icons__WEBPACK_IMPORTED_MODULE_2__.partyIcon,
            onClick: () => {
                this._commands
                    .execute('docmanager:open', {
                    path: panel.context.path,
                    factory: 'Mercury',
                    options: {
                        mode: 'split-right',
                        ref: panel.id
                    }
                })
                    .then(widget => {
                    if (widget instanceof _lumino_widgets__WEBPACK_IMPORTED_MODULE_1__.Widget) {
                        panel.content.disposed.connect(() => {
                            widget.dispose();
                        });
                    }
                });
            }
        });
        panel.toolbar.insertItem(0, 'open-mercury', button);
        return button;
    }
}


/***/ }),

/***/ "./lib/mercury/widget.js":
/*!*******************************!*\
  !*** ./lib/mercury/widget.js ***!
  \*******************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   IMercuryTracker: () => (/* binding */ IMercuryTracker),
/* harmony export */   MercuryWidget: () => (/* binding */ MercuryWidget)
/* harmony export */ });
/* harmony import */ var _jupyterlab_docregistry__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/docregistry */ "webpack/sharing/consume/default/@jupyterlab/docregistry");
/* harmony import */ var _jupyterlab_docregistry__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_docregistry__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @lumino/coreutils */ "webpack/sharing/consume/default/@lumino/coreutils");
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_lumino_coreutils__WEBPACK_IMPORTED_MODULE_1__);


class MercuryWidget extends _jupyterlab_docregistry__WEBPACK_IMPORTED_MODULE_0__.DocumentWidget {
    constructor(context, content) {
        super({ context, content });
        this.title.label = context.localPath;
        this.title.closable = true;
        this.addClass('jp-NotebookPanel');
    }
}
/**
 * The Mercury tracker token.
 */
const IMercuryTracker = new _lumino_coreutils__WEBPACK_IMPORTED_MODULE_1__.Token('@mljar:IMercuryTracker');


/***/ }),

/***/ "./lib/widgets/index.js":
/*!******************************!*\
  !*** ./lib/widgets/index.js ***!
  \******************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   widgets: () => (/* binding */ widgets)
/* harmony export */ });
/* harmony import */ var _jupyter_widgets_base__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyter-widgets/base */ "webpack/sharing/consume/default/@jupyter-widgets/base");
/* harmony import */ var _jupyter_widgets_base__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyter_widgets_base__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyter_widgets_jupyterlab_manager__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyter-widgets/jupyterlab-manager */ "webpack/sharing/consume/default/@jupyter-widgets/jupyterlab-manager");
/* harmony import */ var _jupyter_widgets_jupyterlab_manager__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyter_widgets_jupyterlab_manager__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _mercury_widget__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../mercury/widget */ "./lib/mercury/widget.js");



function* widgetRenderers(editor) {
    for (const w of editor.cellWidgets) {
        if (w instanceof _jupyter_widgets_jupyterlab_manager__WEBPACK_IMPORTED_MODULE_1__.WidgetRenderer) {
            yield w;
        }
    }
}
/**
 * A plugin to add support for rendering Jupyter Widgets.
 */
const widgets = {
    id: '@mljar/mercury-support-ipywidgets',
    autoStart: true,
    optional: [_mercury_widget__WEBPACK_IMPORTED_MODULE_2__.IMercuryTracker, _jupyter_widgets_base__WEBPACK_IMPORTED_MODULE_0__.IJupyterWidgetRegistry],
    activate: (app, mercuryTracker, widgetRegistry) => {
        if (!widgetRegistry) {
            return;
        }
        mercuryTracker === null || mercuryTracker === void 0 ? void 0 : mercuryTracker.forEach(widget => {
            (0,_jupyter_widgets_jupyterlab_manager__WEBPACK_IMPORTED_MODULE_1__.registerWidgetManager)(widget.context, widget.content.rendermime, widgetRenderers(widget.content));
        });
        mercuryTracker === null || mercuryTracker === void 0 ? void 0 : mercuryTracker.widgetAdded.connect((sender, widget) => {
            (0,_jupyter_widgets_jupyterlab_manager__WEBPACK_IMPORTED_MODULE_1__.registerWidgetManager)(widget.context, widget.content.rendermime, widgetRenderers(widget.content));
        });
    }
};


/***/ }),

/***/ "./style/icons/party.svg":
/*!*******************************!*\
  !*** ./style/icons/party.svg ***!
  \*******************************/
/***/ ((module) => {

module.exports = "<svg xmlns=\"http://www.w3.org/2000/svg\" class=\"icon icon-tabler icon-tabler-confetti\" width=\"24\" height=\"24\" viewBox=\"0 0 24 24\" stroke-width=\"2\" stroke=\"currentColor\" fill=\"none\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><path stroke=\"none\" d=\"M0 0h24v24H0z\" fill=\"none\"/><path d=\"M4 5h2\" /><path d=\"M5 4v2\" /><path d=\"M11.5 4l-.5 2\" /><path d=\"M18 5h2\" /><path d=\"M19 4v2\" /><path d=\"M15 9l-1 1\" /><path d=\"M18 13l2 -.5\" /><path d=\"M18 19h2\" /><path d=\"M19 18v2\" /><path d=\"M14 16.518l-6.518 -6.518l-4.39 9.58a1 1 0 0 0 1.329 1.329l9.579 -4.39z\" /></svg>";

/***/ })

}]);
//# sourceMappingURL=lib_index_js.7fe26ffef66ae8eb58e9.js.map