var RecipesBox = React.createClass({
    loadRecipesFromAPI: function () {
        $.ajax({
            url: this.props.api_url + "/recipe",
            dataType: 'json',
            cache: false,
            success: function (data) {
                this.setState({
                    buildAnnouncements: this.state.buildAnnouncements,
                    recipes: data._embedded.recipe
                });
            }.bind(this),
            error: function (xhr, status, err) {
                console.error(this.props.api_url, status, err.toString());
            }.bind(this)
        });
    },
    getInitialState: function () {
        return {
            buildAnnouncements: [],
            recipes: []
        };
    },
    componentDidMount: function () {
        this.loadRecipesFromAPI();
        setInterval(this.loadRecipesFromAPI, this.props.pollInterval);
    },
    announceBuild: function (recipe) {
        console.info(recipe);
        this.setState({
            buildAnnouncements: [recipe],
            recipes: this.state.recipes
        });
    },
    buildMessageRemoved: function () {
        console.debug('buildMessageRemoved');
        this.setState({
            buildAnnouncements: [],
            recipes: this.state.recipes
        });
    },
    render: function () {
        return (
            <div>
                <BuildMessageList buildMessageRemoved={this.buildMessageRemoved}
                                  buildAnnouncements={this.state.buildAnnouncements}/>
                <RecipesTable api_url={this.props.api_url} announceBuildCallback={this.announceBuild}
                              recipes={this.state.recipes} buildMessageRemoved={this.buildMessageRemoved}/>
            </div>
        );
    }
});

var RecipesTable = React.createClass({
    render: function () {

        var buildMessageRemoved = this.props.buildMessageRemoved;

        return (
            <div className="table-responsive">
                <table className="table table-bordered table-hover table-striped centered-text">
                    <thead>
                    <tr>
                        <th>Recipe Id</th>
                        <th>VCS</th>
                        <th>Repository</th>
                        <th>Branch</th>
                        <th>Command</th>
                        <th>Action</th>
                    </tr>
                    </thead>
                    <RecipeList announceBuildCallback={this.props.announceBuildCallback}
                                api_url={this.props.api_url} recipes={this.props.recipes}
                                buildMessageRemoved={buildMessageRemoved}
                    />
                </table>
            </div>
        );
    }
});

var RecipeList = React.createClass({
    render: function () {
        var api_url = this.props.api_url;
        var announceBuildCallback = this.props.announceBuildCallback;
        var buildMessageRemoved = this.props.buildMessageRemoved;
        var recipeNodes = this.props.recipes.map(function (recipe) {
            return (
                <Recipe key={recipe.id} recipe={recipe} api_url={api_url}
                        buildMessageRemoved={buildMessageRemoved}
                        announceBuildCallback={announceBuildCallback}> </Recipe>
            );
        });
        return (
            <tbody>
            {recipeNodes}
            </tbody>
        );
    }
});


var Recipe = React.createClass({

    handleRecipeTrigger: function (e) {
        e.preventDefault();
        var build_desc = JSON.stringify({
            "repository": this.props.recipe.repository.name,
            "branch": this.props.recipe.repository.branch,
            "scm": this.props.recipe.repository.vcs,
            "recipe_id": this.props.recipe.id
        });
        this.props.announceBuildCallback(this.props.recipe);

        $.ajax({
            url: this.props.api_url + '/webhooks/webhawk',
            dataType: 'json',
            type: 'POST',
            data: build_desc,
            success: function (data) {
                // console.info(data);
            }.bind(this),
            error: function (xhr, status, err) {
                console.error(this.props.api_url, status, err.toString());
            }.bind(this)
        });

        setTimeout(this.props.buildMessageRemoved, 10000);
    },
    rawMarkup: function () {
        var rawMarkup = this.props.children.toString();
        return {__html: rawMarkup};
    },

    render: function () {
        return (
            <tr>
                <td>{this.props.recipe.id}</td>
                <td>{this.props.recipe.repository.vcs}</td>
                <td>{this.props.recipe.repository.url}</td>
                <td>{this.props.recipe.repository.branch}</td>
                <td><code>{this.props.recipe.command ? this.props.recipe.command : "-"}</code></td>
                <td>
                    <button type="submit" onClick={this.handleRecipeTrigger} className="btn btn-primary">Trigger
                    </button>
                </td>
            </tr>
        );
    }
});


var BuildMessageList = React.createClass({

    render: function () {
        var buildMessageRemoved = this.props.buildMessageRemoved;
        var messages = this.props.buildAnnouncements.map(function (buildAnnouncement) {
            return (
                <BuildMessage key={buildAnnouncement.id} buildAnnouncement={buildAnnouncement}
                              buildMessageRemoved={buildMessageRemoved}> </BuildMessage>
            );
        });
        return (
            <div className="row">
                <div className="col-lg-12">
                    {messages}
                </div>
            </div>
        );
    }
});

var BuildMessage = React.createClass({
    render: function () {
        return (
            <div className="alert alert-info alert-dismissable">
                <button type="button" className="close" onClick={this.props.buildMessageRemoved}
                        aria-hidden="true">&times;</button>
                <i className="fa fa-info-circle"></i> Build started for
                recipe: <strong>{this.props.buildAnnouncement.id}</strong>
            </div>
        );
    }
});


ReactDOM.render(
    <RecipesBox pollInterval={120000} api_url="/api"/>,
    document.getElementById('recipes-table-container')
);

//  ====================================================


var CommentBox = React.createClass({
    loadCommentsFromServer: function () {
        // tutorial8.js
        var data = [
            {id: 1, author: "Pete Hunt", text: "This is one comment"},
            {id: 2, author: "Jordan Walke", text: "This is *another* comment"}
        ];
        this.setState({data: data});
    },
    getInitialState: function () {
        // tutorial8.js
        var data = [
            {id: 1, author: "Pete Hunt", text: "This is one comment"},
            {id: 2, author: "Jordan Walke", text: "This is *another* comment"}
        ];
        return {data: data};
    },
    handleCommentSubmit: function (comment) {
        var comments = this.state.data;
        // Optimistically set an id on the new comment. It will be replaced by an
        // id generated by the server. In a production application you would likely
        // not use Date.now() for this and would have a more robust system in place.
        comment.id = Date.now();
        var newComments = comments.concat([comment]);
        this.setState({data: newComments});

        $.ajax({
            url: this.props.url,
            dataType: 'json',
            type: 'POST',
            data: comment,
            success: function (data) {
                this.setState({data: data});
            }.bind(this),
            error: function (xhr, status, err) {
                console.error(this.props.url, status, err.toString());
            }.bind(this)
        });
    },
    componentDidMount: function () {
        this.loadCommentsFromServer();
        setInterval(this.loadCommentsFromServer, this.props.pollInterval);
    },
    render: function () {
        return (
            <div className="commentBox">
                <h1>Comments</h1>
                <CommentList data={this.state.data}/>
                <CommentForm onCommentSubmit={this.handleCommentSubmit}/>
            </div>
        );
    }
});

// tutorial10.js
var CommentList = React.createClass({
    render: function () {
        var commentNodes = this.props.data.map(function (comment) {
            return (
                <Comment author={comment.author} key={comment.id}>
                    {comment.text}
                </Comment>
            );
        });
        return (
            <div className="commentList">
                {commentNodes}
            </div>
        );
    }
});


var CommentForm = React.createClass({
    getInitialState: function () {
        return {author: '', text: ''};
    },
    handleAuthorChange: function (e) {
        this.setState({author: e.target.value});
    },
    handleTextChange: function (e) {
        this.setState({text: e.target.value});
    },
    handleSubmit: function (e) {
        e.preventDefault();

        var author = this.state.author.trim();
        var text = this.state.text.trim();
        if (!text || !author) {
            return;
        }
        this.props.onCommentSubmit({author: author, text: text});
        this.setState({author: '', text: ''});
    },
    render: function () {
        return (
            <div className="commentForm">
                <form className="commentForm" onSubmit={this.handleSubmit}>
                    <input
                        type="text"
                        placeholder="Your name"
                        value={this.state.author}
                        onChange={this.handleAuthorChange}
                    />
                    <input
                        type="text"
                        placeholder="Say something..."
                        value={this.state.text}
                        onChange={this.handleTextChange}
                    />
                    <input type="submit" value="Post"/>
                </form>
                <div className="commentPreview">
                    <hr/>
                    <b>Preview >></b>
                    <Comment author={this.state.author} key={1}>
                        {this.state.text}
                    </Comment>
                </div>
            </div>
        );
    }
});

// tutorial8.js
var data = [
    {id: 1, author: "Dimi Bal", text: "This is one comment"},
    {id: 2, author: "Dzim", text: "This is *another* comment"}
];

// tutorial4.js
// tutorial6.js
var Comment = React.createClass({

    rawMarkup: function () {
        var rawMarkup = this.props.children.toString();
        return {__html: rawMarkup};
    },

    render: function () {
        return (
            <div className="comment">
                <h2 className="commentAuthor">
                    {this.props.author}
                </h2>
                <span>asdasd</span>
            </div>
        );
    }
});
