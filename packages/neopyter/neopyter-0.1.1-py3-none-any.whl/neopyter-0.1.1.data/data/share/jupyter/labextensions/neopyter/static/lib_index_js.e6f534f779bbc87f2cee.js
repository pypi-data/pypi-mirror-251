"use strict";
(self["webpackChunkneopyter"] = self["webpackChunkneopyter"] || []).push([["lib_index_js"],{

/***/ "./lib/error.js":
/*!**********************!*\
  !*** ./lib/error.js ***!
  \**********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   RPCError: () => (/* binding */ RPCError)
/* harmony export */ });
class RPCError extends Error {
    constructor(message) {
        super(message);
        this.name = 'RPCError';
    }
}


/***/ }),

/***/ "./lib/icons.js":
/*!**********************!*\
  !*** ./lib/icons.js ***!
  \**********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   statusPageIcon: () => (/* binding */ statusPageIcon)
/* harmony export */ });
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _style_icons_statuspage_svg__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../style/icons/statuspage.svg */ "./style/icons/statuspage.svg");


const statusPageIcon = new _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__.LabIcon({
    name: 'neopyter:status-page',
    svgstr: _style_icons_statuspage_svg__WEBPACK_IMPORTED_MODULE_1__
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
/* harmony import */ var _jupyterlab_services__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/services */ "webpack/sharing/consume/default/@jupyterlab/services");
/* harmony import */ var _jupyterlab_services__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_services__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/coreutils */ "webpack/sharing/consume/default/@jupyterlab/coreutils");
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_application__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/application */ "webpack/sharing/consume/default/@jupyterlab/application");
/* harmony import */ var _jupyterlab_application__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_application__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @jupyterlab/notebook */ "webpack/sharing/consume/default/@jupyterlab/notebook");
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _jupyterlab_docmanager__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @jupyterlab/docmanager */ "webpack/sharing/consume/default/@jupyterlab/docmanager");
/* harmony import */ var _jupyterlab_docmanager__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_docmanager__WEBPACK_IMPORTED_MODULE_4__);
/* harmony import */ var remeda__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! remeda */ "webpack/sharing/consume/default/remeda/remeda");
/* harmony import */ var remeda__WEBPACK_IMPORTED_MODULE_5___default = /*#__PURE__*/__webpack_require__.n(remeda__WEBPACK_IMPORTED_MODULE_5__);
/* harmony import */ var _rpcServer__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! ./rpcServer */ "./lib/rpcServer.js");
/* harmony import */ var _transport__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! ./transport */ "./lib/transport/websocketTransport.js");
/* harmony import */ var _statusidepanel__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ./statusidepanel */ "./lib/statusidepanel.js");
/* harmony import */ var _icons__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ./icons */ "./lib/icons.js");










/**
 * Initialization data for the neopyter extension. */
const neopyterPlugin = {
    id: 'neopyter',
    description: 'A JupyterLab extension.',
    autoStart: true,
    requires: [_jupyterlab_docmanager__WEBPACK_IMPORTED_MODULE_4__.IDocumentManager, _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_3__.INotebookTracker, _jupyterlab_application__WEBPACK_IMPORTED_MODULE_2__.ILayoutRestorer],
    activate: (app, docmanager, nbtracker, restorer) => {
        console.log('JupyterLab extension noejupy is activated!');
        const sidebar = new _statusidepanel__WEBPACK_IMPORTED_MODULE_6__.StatusSidePanel();
        sidebar.title.caption = 'Neopyter';
        sidebar.title.icon = _icons__WEBPACK_IMPORTED_MODULE_7__.statusPageIcon;
        app.shell.add(sidebar, 'right');
        if (restorer) {
            restorer.add(sidebar, '@neopyter/graphsidebar');
        }
        const settings = _jupyterlab_services__WEBPACK_IMPORTED_MODULE_0__.ServerConnection.makeSettings();
        const url = _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_1__.URLExt.join(settings.wsUrl, 'neopyter', 'channel');
        const getCurrentNotebook = () => {
            const widget = nbtracker.currentWidget;
            if (widget) {
                app.shell.activateById(widget.id);
            }
            return widget === null || widget === void 0 ? void 0 : widget.content;
        };
        const getNotebookModel = (path) => {
            var _a, _b;
            const notebookPanel = docmanager.findWidget(path);
            let notebook = notebookPanel === null || notebookPanel === void 0 ? void 0 : notebookPanel.content;
            if ((_a = nbtracker.currentWidget) === null || _a === void 0 ? void 0 : _a.isUntitled) {
                notebook = nbtracker.currentWidget.content;
            }
            const sharedModel = (_b = notebook === null || notebook === void 0 ? void 0 : notebook.model) === null || _b === void 0 ? void 0 : _b.sharedModel;
            if (!notebookPanel || !sharedModel || !notebook) {
                throw `Can't find ${path} or select untitled ipynb`;
            }
            return {
                notebookPanel,
                notebook,
                sharedModel
            };
        };
        const getCellModel = (path, cellIdx) => {
            const { notebook, sharedModel: sharedNotebookModel } = getNotebookModel(path);
            const sharedModel = sharedNotebookModel.getCell(cellIdx);
            return {
                notebook,
                sharedNotebookModel,
                sharedModel
            };
        };
        const dispatcher = {
            echo: (message) => {
                const msg = `hello: ${message}`;
                return msg;
            },
            executeCommand: async (command) => {
                await app.commands.execute(command);
            }
        };
        const docmanagerDispatcher = {
            getCurrentNotebook: () => {
                const notebookPanel = nbtracker.currentWidget;
                if (notebookPanel) {
                    const context = docmanager.contextForWidget(notebookPanel);
                    return context === null || context === void 0 ? void 0 : context.localPath;
                }
            },
            isFileOpen: (path) => {
                return !!docmanager.findWidget(path);
            },
            isFileExist: async (path) => {
                try {
                    return !!(await docmanager.services.contents.get(path));
                }
                catch (e) {
                    if (e.response.status !== 404) {
                        throw e;
                    }
                    return false;
                }
            },
            createNew: (path, widgetName, kernel) => {
                return docmanager.createNew(path, widgetName, kernel);
            },
            openFile: (path) => {
                return !!docmanager.open(path);
            },
            openOrReveal: (path) => {
                return !!docmanager.openOrReveal(path);
            },
            closeFile: async (path) => {
                return await docmanager.closeFile(path);
            },
            selectAbove: () => {
                const notebook = getCurrentNotebook();
                notebook && _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_3__.NotebookActions.selectBelow(notebook);
            },
            selectBelow: () => {
                const notebook = getCurrentNotebook();
                notebook && _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_3__.NotebookActions.selectBelow(notebook);
            }
        };
        const notebookDispatcher = {
            getCellNum: (path) => {
                return getNotebookModel(path).sharedModel.cells.length;
            },
            setCellNum: (path, num) => {
                const { notebook, sharedModel } = getNotebookModel(path);
                const currentNum = sharedModel.cells.length;
                if (num > currentNum) {
                    sharedModel.insertCells(currentNum, remeda__WEBPACK_IMPORTED_MODULE_5__.range(0, num - currentNum).map(() => ({
                        cell_type: notebook.notebookConfig.defaultCell,
                        metadata: notebook.notebookConfig.defaultCell === 'code' ? { trusted: true } : {}
                    })));
                    return;
                }
                while (num < sharedModel.cells.length) {
                    sharedModel.deleteCell(sharedModel.cells.length - 1);
                }
            },
            getCell: (path, index) => {
                const { sharedModel } = getCellModel(path, index);
                return sharedModel.toJSON();
            },
            deleteCell: (path, index) => {
                return getNotebookModel(path).sharedModel.deleteCell(index);
            },
            insertCell: (path, index) => {
                const { notebook, sharedModel } = getNotebookModel(path);
                return sharedModel.insertCell(index, {
                    cell_type: notebook.notebookConfig.defaultCell,
                    metadata: notebook.notebookConfig.defaultCell === 'code' ? { trusted: true } : {}
                });
            },
            activateCell: (path, index) => {
                const { notebook } = getNotebookModel(path);
                notebook.activeCellIndex = index;
            },
            scrollToItem: (path, index, align, margin) => {
                const { notebook } = getNotebookModel(path);
                notebook.scrollToItem(index, align, margin);
            },
            syncCells: (path, from, cells) => {
                const { notebook, sharedModel: sharedNotebookModel } = getNotebookModel(path);
                cells.forEach((cell, idx) => {
                    const index = from + idx;
                    const cellModel = sharedNotebookModel.getCell(index);
                    if (cellModel) {
                        if (cell.cell_type === undefined || cellModel.cell_type === cell.cell_type) {
                            cellModel.setSource(cell.source);
                        }
                        else {
                            sharedNotebookModel.deleteCell(idx);
                            sharedNotebookModel.insertCell(idx, {
                                cell_type: cell.cell_type,
                                source: cell.source,
                                metadata: cellModel.getMetadata()
                            });
                        }
                        return;
                    }
                    sharedNotebookModel.insertCell(index, {
                        cell_type: cell.cell_type,
                        source: cell.source,
                        metadata: notebook.notebookConfig.defaultCell === 'code'
                            ? {
                                // This is an empty cell created by user, thus is trusted
                                trusted: true
                            }
                            : {}
                    });
                });
            },
            save: async (path) => {
                const { notebookPanel } = getNotebookModel(path);
                const context = docmanager.contextForWidget(notebookPanel);
                context === null || context === void 0 ? void 0 : context.path;
                return await (context === null || context === void 0 ? void 0 : context.save());
            },
            runSelectedCell: async (path) => {
                return await app.commands.execute('notebook:run-cell');
            },
            runAllAbove: async (path) => {
                return await app.commands.execute('notebook:run-all-above');
            },
            runAllBelow: async (path) => {
                return await app.commands.execute('notebook:run-all-below');
            },
            runAll: async (path) => {
                return await app.commands.execute('notebook:run-all-cells');
            },
            restartKernel: async (path) => {
                const { notebookPanel } = getNotebookModel(path);
                return await notebookPanel.sessionContext.restartKernel();
            },
            restartRunAll: async (path) => {
                const { notebookPanel } = getNotebookModel(path);
                await notebookPanel.sessionContext.restartKernel();
                return await app.commands.execute('notebook:run-all-cells');
            }
        };
        const cellDispatcher = {
            setCellSource: (path, cellIdx, source) => {
                const { sharedModel } = getCellModel(path, cellIdx);
                sharedModel.setSource(source);
            },
            setCellType: (path, cellIdx, type) => {
                const { sharedNotebookModel, sharedModel } = getCellModel(path, cellIdx);
                if (sharedModel.cell_type !== type) {
                    sharedNotebookModel.deleteCell(cellIdx);
                    sharedNotebookModel.insertCell(cellIdx, {
                        cell_type: type,
                        source: sharedModel.getSource(),
                        metadata: sharedModel.getMetadata()
                    });
                }
            }
        };
        Object.assign(dispatcher, docmanagerDispatcher);
        Object.assign(dispatcher, notebookDispatcher);
        Object.assign(dispatcher, cellDispatcher);
        const server = new _rpcServer__WEBPACK_IMPORTED_MODULE_8__.RpcServer(dispatcher);
        server.start(_transport__WEBPACK_IMPORTED_MODULE_9__.WebsocketTransport, url);
    }
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = ([neopyterPlugin]);


/***/ }),

/***/ "./lib/msgpackRpcProtocol.js":
/*!***********************************!*\
  !*** ./lib/msgpackRpcProtocol.js ***!
  \***********************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   MessageType: () => (/* binding */ MessageType),
/* harmony export */   deserializeMessage: () => (/* binding */ deserializeMessage),
/* harmony export */   deserializeStream: () => (/* binding */ deserializeStream),
/* harmony export */   serializeMessage: () => (/* binding */ serializeMessage)
/* harmony export */ });
/* harmony import */ var _msgpack_msgpack__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @msgpack/msgpack */ "./node_modules/.pnpm/@msgpack+msgpack@3.0.0-beta2/node_modules/@msgpack/msgpack/dist.es5+esm/decode.mjs");
/* harmony import */ var _msgpack_msgpack__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @msgpack/msgpack */ "./node_modules/.pnpm/@msgpack+msgpack@3.0.0-beta2/node_modules/@msgpack/msgpack/dist.es5+esm/encode.mjs");
/* harmony import */ var _msgpack_msgpack__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @msgpack/msgpack */ "./node_modules/.pnpm/@msgpack+msgpack@3.0.0-beta2/node_modules/@msgpack/msgpack/dist.es5+esm/decodeAsync.mjs");
/* harmony import */ var _error__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./error */ "./lib/error.js");


const errorRef = 'https://github.com/msgpack-rpc/msgpack-rpc/blob/master/spec.md';
var MessageType;
(function (MessageType) {
    MessageType[MessageType["Request"] = 0] = "Request";
    MessageType[MessageType["Response"] = 1] = "Response";
    MessageType[MessageType["Notification"] = 2] = "Notification";
})(MessageType || (MessageType = {}));
function deserializeMessage(data) {
    const message = (0,_msgpack_msgpack__WEBPACK_IMPORTED_MODULE_0__.decode)(data);
    if (!Array.isArray(message) || (message.length !== 4 && message.length !== 3)) {
        throw new _error__WEBPACK_IMPORTED_MODULE_1__.RPCError(`Invalid msgpack-rpc message: ${JSON.stringify(message)}, please reference ${errorRef}`);
    }
    const msgType = message[0];
    if (msgType !== 0 && msgType !== 1 && msgType !== 2) {
        throw new _error__WEBPACK_IMPORTED_MODULE_1__.RPCError(`Invalid msgpack-rpc message: ${JSON.stringify(message)}, please reference ${errorRef}`);
    }
    if (msgType === MessageType.Request) {
        return { type: MessageType.Request, msgid: message[1], method: message[2], params: message[3] };
    }
    else if (msgType === MessageType.Response) {
        return { type: MessageType.Response, msgid: message[1], error: message[2], result: message[3] };
    }
    return { type: MessageType.Notification, method: message[1], params: message[2] };
}
function serializeMessage(message) {
    if (message.type === MessageType.Request) {
        return (0,_msgpack_msgpack__WEBPACK_IMPORTED_MODULE_2__.encode)([message.type, message.msgid, message.method, message.params]);
    }
    else if (message.type === MessageType.Response) {
        return (0,_msgpack_msgpack__WEBPACK_IMPORTED_MODULE_2__.encode)([message.type, message.msgid, message.error ? message.error.toString() : undefined, message.result]);
    }
    return (0,_msgpack_msgpack__WEBPACK_IMPORTED_MODULE_2__.encode)([message.type, message.method, message.params]);
}
async function* deserializeStream(stream) {
    // const ss = decodeArrayStream(stream);
    const ss = (0,_msgpack_msgpack__WEBPACK_IMPORTED_MODULE_3__.decodeMultiStream)(stream);
    for await (const message of ss) {
        if (!Array.isArray(message) || (message.length !== 4 && message.length !== 3)) {
            throw new _error__WEBPACK_IMPORTED_MODULE_1__.RPCError(`Invalid msgpack-rpc message: ${JSON.stringify(message)}, please reference ${errorRef}`);
        }
        const msgType = message[0];
        if (msgType !== 0 && msgType !== 1 && msgType !== 2) {
            throw new _error__WEBPACK_IMPORTED_MODULE_1__.RPCError(`Invalid msgpack-rpc message: ${JSON.stringify(message)}, please reference ${errorRef}`);
        }
        if (msgType === MessageType.Request) {
            yield { type: MessageType.Request, msgid: message[1], method: message[2], params: message[3] };
        }
        else if (msgType === MessageType.Response) {
            yield { type: MessageType.Response, msgid: message[1], error: message[2], result: message[3] };
        }
        else {
            yield { type: MessageType.Notification, method: message[1], params: message[2] };
        }
    }
}


/***/ }),

/***/ "./lib/rpcServer.js":
/*!**************************!*\
  !*** ./lib/rpcServer.js ***!
  \**************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   RpcServer: () => (/* binding */ RpcServer)
/* harmony export */ });
/* harmony import */ var _msgpackRpcProtocol__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./msgpackRpcProtocol */ "./lib/msgpackRpcProtocol.js");
/* harmony import */ var _error__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./error */ "./lib/error.js");


class RpcServer {
    constructor(dispatcher) {
        this.dispatcher = dispatcher;
    }
    start(transportCtr, ...params) {
        this.transport = new transportCtr(this, ...params);
    }
    async dispatchMethod(message, responseFn) {
        if (!this.dispatcher[message.method]) {
            const error = new _error__WEBPACK_IMPORTED_MODULE_0__.RPCError(`Method not found ${message.method}`);
            if (message.type === _msgpackRpcProtocol__WEBPACK_IMPORTED_MODULE_1__.MessageType.Request && responseFn) {
                responseFn({
                    type: _msgpackRpcProtocol__WEBPACK_IMPORTED_MODULE_1__.MessageType.Response,
                    msgid: message.msgid,
                    error,
                    result: undefined
                });
            }
            throw error;
        }
        try {
            const result = await this.dispatcher[message.method](...message.params);
            if (message.type === _msgpackRpcProtocol__WEBPACK_IMPORTED_MODULE_1__.MessageType.Request && responseFn) {
                responseFn({
                    type: _msgpackRpcProtocol__WEBPACK_IMPORTED_MODULE_1__.MessageType.Response,
                    msgid: message.msgid,
                    result: result
                });
            }
        }
        catch (error) {
            console.error(error);
            if (message.type === _msgpackRpcProtocol__WEBPACK_IMPORTED_MODULE_1__.MessageType.Request && responseFn) {
                responseFn({
                    type: _msgpackRpcProtocol__WEBPACK_IMPORTED_MODULE_1__.MessageType.Response,
                    msgid: message.msgid,
                    error: error
                });
            }
        }
    }
}


/***/ }),

/***/ "./lib/statusidepanel.js":
/*!*******************************!*\
  !*** ./lib/statusidepanel.js ***!
  \*******************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   StatusSidePanel: () => (/* binding */ StatusSidePanel)
/* harmony export */ });
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/coreutils */ "webpack/sharing/consume/default/@jupyterlab/coreutils");
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/services */ "webpack/sharing/consume/default/@jupyterlab/services");
/* harmony import */ var _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_2__);



class StatusSidePanel extends _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_2__.SidePanel {
    constructor() {
        super();
        this.id = 'neopyter-status-sidepanel';
        const settings = _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__.ServerConnection.makeSettings();
        const url = _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__.URLExt.join(settings.baseUrl, 'neopyter', 'tcp_server_info');
        setTimeout(async () => {
            const response = await fetch(url);
            if (!response.ok) {
                const p = document.createElement('p');
                this.content.node.appendChild(p);
                p.textContent = 'Access API failed';
                return;
            }
            const { code, message, data } = await response.json();
            if (code !== 0) {
                const p = document.createElement('p');
                this.content.node.appendChild(p);
                p.textContent = message;
                return;
            }
            for (const host of data.hosts) {
                const p = document.createElement('p');
                this.content.node.appendChild(p);
                p.textContent = `${host}:${data.port}`;
            }
        }, 1000);
    }
}


/***/ }),

/***/ "./lib/transport/base.js":
/*!*******************************!*\
  !*** ./lib/transport/base.js ***!
  \*******************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   BaseTransport: () => (/* binding */ BaseTransport)
/* harmony export */ });
/* harmony import */ var _msgpackRpcProtocol__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ../msgpackRpcProtocol */ "./lib/msgpackRpcProtocol.js");

class BaseTransport {
    constructor(server) {
        this.server = server;
    }
    async onRequest(message) {
        await this.server.dispatchMethod(message, (response) => {
            this.sendData((0,_msgpackRpcProtocol__WEBPACK_IMPORTED_MODULE_0__.serializeMessage)(response));
        });
    }
    async onNotify(message) {
        this.server.dispatchMethod(message);
    }
}


/***/ }),

/***/ "./lib/transport/websocketTransport.js":
/*!*********************************************!*\
  !*** ./lib/transport/websocketTransport.js ***!
  \*********************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   WebsocketTransport: () => (/* binding */ WebsocketTransport)
/* harmony export */ });
/* harmony import */ var _base__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./base */ "./lib/transport/base.js");
/* harmony import */ var _msgpackRpcProtocol__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../msgpackRpcProtocol */ "./lib/msgpackRpcProtocol.js");
/* harmony import */ var _error__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../error */ "./lib/error.js");



function base64ToBytes(str) {
    const binString = atob(str);
    return Uint8Array.from(binString, m => m.codePointAt(0));
}
function bytesToBase64(bytes) {
    const binString = String.fromCodePoint(...bytes);
    return btoa(binString);
}
class WebsocketTransport extends _base__WEBPACK_IMPORTED_MODULE_0__.BaseTransport {
    constructor(server, url) {
        super(server);
        this.url = url;
        this.websocket = new WebSocket(this.url);
        this.websocket.binaryType = 'arraybuffer';
        this.readableStream = new ReadableStream({
            start: controller => {
                // console.log('start');
                this.websocket.addEventListener('open', event => {
                    this.onOpen(event);
                });
                this.websocket.addEventListener('message', event => {
                    const buf = base64ToBytes(event.data);
                    controller.enqueue(buf);
                });
                this.websocket.addEventListener('error', event => {
                    this.onError(event);
                    throw event;
                });
                this.websocket.addEventListener('close', event => {
                    this.onClose(event);
                    controller.close();
                });
            }
        });
        setTimeout(async () => {
            for await (const message of (0,_msgpackRpcProtocol__WEBPACK_IMPORTED_MODULE_1__.deserializeStream)(this.readableStream)) {
                // console.log(message);
                this.onRead(message);
            }
        }, 0);
    }
    async onRead(message) {
        switch (message.type) {
            case _msgpackRpcProtocol__WEBPACK_IMPORTED_MODULE_1__.MessageType.Request:
                await this.onRequest(message);
                break;
            case _msgpackRpcProtocol__WEBPACK_IMPORTED_MODULE_1__.MessageType.Notification:
                await this.onNotify(message);
                break;
            default:
                throw new _error__WEBPACK_IMPORTED_MODULE_2__.RPCError(`Unknown message: ${message}`);
        }
    }
    sendData(data) {
        this.websocket.send(bytesToBase64(data));
    }
    onOpen(_event) {
        console.log(`Connection to neopyter jupyter server by websocket ${this.websocket.url}`);
    }
    onError(event) {
        console.error('Websocket error', event);
    }
    onClose(_event) {
        console.log(`DisConnection to neopyter jupyter server by websocket ${this.websocket.url}`);
    }
}


/***/ }),

/***/ "./style/icons/statuspage.svg":
/*!************************************!*\
  !*** ./style/icons/statuspage.svg ***!
  \************************************/
/***/ ((module) => {

module.exports = "<svg t=\"1704342603868\" class=\"icon\" viewBox=\"0 0 1024 1024\" version=\"1.1\" xmlns=\"http://www.w3.org/2000/svg\" p-id=\"1462\" width=\"200\" height=\"200\"><path d=\"M512.416 409.472a239.914667 239.914667 0 1 1 0 479.786667 239.914667 239.914667 0 0 1 0-479.786667zM6.645333 371.925333l128.853334 152.490667a27.264 27.264 0 0 0 38.954666 2.901333c208.426667-186.837333 468.053333-186.837333 675.84 0a27.392 27.392 0 0 0 39.082667-2.901333l128.256-152.490667a27.562667 27.562667 0 0 0-3.2-38.656c-302.933333-264.704-702.378667-264.704-1005.013333 0a27.733333 27.733333 0 0 0-2.773334 38.656z\" p-id=\"1463\"></path></svg>\n";

/***/ })

}]);
//# sourceMappingURL=lib_index_js.e6f534f779bbc87f2cee.js.map