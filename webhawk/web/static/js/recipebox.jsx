let RecipesBox = React.createClass({
    loadRecipesFromAPI: () => {
        $.ajax({
            url: this.props.api_url + "/recipe",
            dataType: 'json',
            cache: false,
            success: ((data) => {
                this.setState({
                    buildAnnouncements: this.state.buildAnnouncements,
                    recipes: data._embedded.recipe
                });
            }).bind(this),
            error: ((xhr, status, err) => {
                console.error(this.props.api_url, status, err.toString());
            }).bind(this)
        });
    },
    getInitialState: () => {
        return {
            buildAnnouncements: [],
            recipes: []
        };
    },
    componentDidMount: () => {
        this.loadRecipesFromAPI();
        setInterval(this.loadRecipesFromAPI, this.props.pollInterval);
    },
    announceBuild: (recipe) => {
        console.info(recipe);
        this.setState({
            buildAnnouncements: [recipe],
            recipes: this.state.recipes
        });
    },
    buildMessageRemoved: () => {
        console.debug('buildMessageRemoved');
        this.setState({
            buildAnnouncements: [],
            recipes: this.state.recipes
        });
    },
    render: () => {
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

let RecipesTable = React.createClass({
    render: () => {

        const buildMessageRemoved = this.props.buildMessageRemoved;

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

let RecipeList = React.createClass({
    render: () => {
        const api_url = this.props.api_url;
        const announceBuildCallback = this.props.announceBuildCallback;
        const buildMessageRemoved = this.props.buildMessageRemoved;
        let recipeNodes = this.props.recipes.map((recipe) => {
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


let Recipe = React.createClass({

    handleRecipeTrigger: (e) => {
        e.preventDefault();
        let build_desc = JSON.stringify({
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
            success: ((data) => {
                // console.info(data);
            }).bind(this),
            error: ((xhr, status, err) => {
                console.error(this.props.api_url, status, err.toString());
            }).bind(this)
        });

        setTimeout(this.props.buildMessageRemoved, 10000);
    },
    rawMarkup: () => {
        let rawMarkup = this.props.children.toString();
        return {__html: rawMarkup};
    },

    render: () => {
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


let BuildMessageList = React.createClass({

    render: () => {
        const buildMessageRemoved = this.props.buildMessageRemoved;
        let messages = this.props.buildAnnouncements.map((buildAnnouncement) => {
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

let BuildMessage = React.createClass({
    render: () => {
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


let CommentBox = React.createClass({
    loadCommentsFromServer: () => {
        // tutorial8.js
        const data = [
            {id: 1, author: "Pete Hunt", text: "This is one comment"},
            {id: 2, author: "Jordan Walke", text: "This is *another* comment"}
        ];
        this.setState({data: data});
    },
    getInitialState: () => {
        // tutorial8.js
        const data = [
            {id: 1, author: "Pete Hunt", text: "This is one comment"},
            {id: 2, author: "Jordan Walke", text: "This is *another* comment"}
        ];
        return {data: data};
    },
    handleCommentSubmit: (comment) => {
        let comments = this.state.data;
        // Optimistically set an id on the new comment. It will be replaced by an
        // id generated by the server. In a production application you would likely
        // not use Date.now() for this and would have a more robust system in place.
        comment.id = Date.now();
        let newComments = comments.concat([comment]);
        this.setState({data: newComments});

        $.ajax({
            url: this.props.url,
            dataType: 'json',
            type: 'POST',
            data: comment,
            success: ((data) => {
                this.setState({data: data});
            }).bind(this),
            error: ((xhr, status, err) => {
                console.error(this.props.url, status, err.toString());
            }).bind(this)
        });
    },
    componentDidMount: (() => {
        this.loadCommentsFromServer();
        setInterval(this.loadCommentsFromServer, this.props.pollInterval);
    }),
    render: () => {
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
let CommentList = React.createClass({
    render: () => {
        let commentNodes = this.props.data.map((comment) => {
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


let CommentForm = React.createClass({
    getInitialState: () => {
        return {author: '', text: ''};
    },
    handleAuthorChange: (e) => {
        this.setState({author: e.target.value});
    },
    handleTextChange: (e) => {
        this.setState({text: e.target.value});
    },
    handleSubmit: (e) => {
        e.preventDefault();

        const author = this.state.author.trim();
        const text = this.state.text.trim();
        if (!text || !author) {
            return;
        }
        this.props.onCommentSubmit({author: author, text: text});
        this.setState({author: '', text: ''});
    },
    render: () => {
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
const data = [
    {id: 1, author: "Dimi Bal", text: "This is one comment"},
    {id: 2, author: "Dzim", text: "This is *another* comment"}
];

// tutorial4.js
// tutorial6.js
let Comment = React.createClass({

    rawMarkup: () => {
        let rawMarkup = this.props.children.toString();
        return {__html: rawMarkup};
    },

    render: () => {
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
