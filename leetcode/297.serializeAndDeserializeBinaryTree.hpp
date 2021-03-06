/*
 *
 *
 297. Serialize and Deserialize Binary Tree

 Serialization is the process of converting a data structure or object into a sequence of bits so that it can be stored in a file or memory buffer, or transmitted across a network connection link to be reconstructed later in the same or another computer environment.

 Design an algorithm to serialize and deserialize a binary tree. There is no restriction on how your serialization/deserialization algorithm should work. You just need to ensure that a binary tree can be serialized to a string and this string can be deserialized to the original tree structure.

 For example, you may serialize the following tree

 1
 / \
 2   3
 / \
 4   5
 as "[1,2,3,null,null,4,5]", just the same as how LeetCode OJ serializes a binary tree. You do not necessarily need to follow this format, so please be creative and come up with different approaches yourself.

Note: Do not use class member/global/static variables to store states. Your serialize and deserialize algorithms should be stateless.

Credits:
Special thanks to @Louis1992 for adding this problem and creating all test cases.

================================================================================
SOLUTION

CRITICAL:
Serialize and deserialize is the same tree traversal process, except the difference that
in deserialize, tree nodes must be constructed from input string first!

But what kind of traversal order?

In order traversal will fail for the following:

0
/
0
and
0
\
0

as both will be treated as #0#0#, because (left,root) and (root, right) can't be
differentiated.

Preorder and postorder traversal will do by storing NULL child nodes.
preorder: 00#, 0#0
postorder: 0#0, #00.
Actually postorder is almost the same as preorder if inspected backward!

FOLLOW UP
--------------------------------------------------------------------------------
Can we adapt inorder traversal to serialize the tree?
(0)0)
(0(0))

*/

/**
 * Definition for a binary tree node.
 * struct TreeNode {
 *     int val;
 *     TreeNode *left;
 *     TreeNode *right;
 *     TreeNode(int x) : val(x), left(NULL), right(NULL) {}
 * };
 */

#pragma once

#include "_type.hpp"
#include "debug.hpp"
//#include <assert.h>
//#include <iostream>
//#include <queue>
//#include <sstream>
//#include <string>

using namespace std;

inline TreeNode* _getNode(istringstream& s)
{
    //if (s.rdbuf()->in_avail() == 0) return NULL; // empty stream
    if (s.eof()) { return NULL; } // empty stream

    string sval;
    //s >> sval;
    getline(s, sval, ',');

    if (sval.compare("") && sval.compare("#") && sval.compare("null") && sval.compare("NULL")) {
        return new TreeNode(stoi(sval));
    }
    return NULL;
}

/**
 * trim leading and trailing "#,"
 *
 */
void trimTrailing(string &s) {
        // trim trailing #
    auto rit = s.rbegin();
    for (rit = s.rbegin(); rit != s.rend() && (*rit == ',' || *rit =='#'); ++rit);
    s.erase(rit.base(), s.end());

    auto it = s.begin();
    for (it = s.begin(); it != s.end() && (*it == ',' || *it == '#'); ++it);
    s.erase(s.begin(), it);
}

class CodecBfs {
public:
    // Encodes a tree to a single string.
    static string serialize(TreeNode* root)
    {
        return serializeBfs(root);
    }

    // Decodes your encoded data to tree.
    static TreeNode* deserialize(string data)
    {
        return deserializeBfs(data);
    }

    static string serializeBfs(TreeNode* root)
    {
        ostringstream out;

        queue<TreeNode*> q; // queue as search frontier for bfs
        TreeNode* treeNode = NULL;

        if (root) { q.push(root); }

        while (q.size()) { // search frontier queue is not empty
            treeNode = q.front();
            q.pop(); // pop out of search frontier

            if (treeNode) {
                q.push(treeNode->left); // add connected nodes(children) to search frontier
                q.push(treeNode->right); // must push NULL children!
            }
            out << (treeNode ? to_string(treeNode->val):"#") << ",";
        }
        string result = out.str();

        // trim trailing "#"
        string::iterator it = result.end() - 1;
        while (it >= result.begin() && ( *it == ',' || *it == '#')) --it;
        result.erase(it + 1, result.end());

        cout << "bfs serialized tree: " << result << endl;

        return result;
    }

    static TreeNode* deserializeBfs(string data)
    {
        //cout << "deserialize data: " << data << endl;
        istringstream in(data);
        queue<TreeNode*> q;

        TreeNode *root, *treeNode, *treeNodeNew = NULL;
        string sval;

        // XXX: of course, memory leaks here. Use smart pointers in production.
        root = treeNodeNew = _getNode(in);
        if (treeNodeNew) q.push(treeNodeNew);

        while (q.size()) { // search frontier queue is not empty
            treeNode = q.front();
            q.pop(); // pop out of search frontier

            if (!treeNode) continue;

            // the only difference between serialize & deserialize
            treeNodeNew = _getNode(in);
            treeNode->left = treeNodeNew;
            treeNodeNew = _getNode(in);
            treeNode->right = treeNodeNew;

            q.push(treeNode->left); // add connected nodes(children) to search frontier
            q.push(treeNode->right);
        }

        return root;
    }
};

class CodecDfsPreorder {
public:
    string serialize(TreeNode *root) {
        //string output = serializeIterative(root);
        string output = serializeRecursive(root);
        trimTrailing(output);

        return output;
    }

    void serializeDfs(TreeNode *root, ostringstream &sout) {
        if (!root) {
            sout << "#,";
            return;
        }
        sout << root->val << ",";
        serializeDfs(root->left, sout);
        serializeDfs(root->right, sout);
    }

    string serializeRecursive(TreeNode *root) {
        ostringstream sout;
        serializeDfs(root, sout);

        return sout.str();
    }

    string serializeIterative(TreeNode *root) {
        ostringstream sout;

        stack<TreeNode*> frontier;
        frontier.push(root);
        while (frontier.size()) {
            TreeNode *pNode = frontier.top(); frontier.pop();
            if (pNode) {
                frontier.push(pNode->right); // preorder: root, left, right
                frontier.push(pNode->left);
                sout << pNode->val << ",";
            } else {
                sout << "#,";
            }
        }

        string output = sout.str();
        // trim trailing #
        auto it = output.rbegin();
        for (it = output.rbegin(); it != output.rend() && (*it == ',' || *it =='#'); ++it);
        output.erase(it.base(), output.end());
        cout << "preorder dfs serialized tree: " << output << endl;

        return output;
    }

    TreeNode* deserialize(string data) {
        //TreeNode *root = deserializeRecursive(data);
        TreeNode *root = deserializeIterative(data);

        return root;
    }

    TreeNode* deserializeDfs(istringstream &sin) {
        TreeNode *pRoot = _getNode(sin);

        if (pRoot) {
            pRoot->left = deserializeDfs(sin);
            pRoot->right = deserializeDfs(sin);
        }

        return pRoot;
    }

    TreeNode* deserializeRecursive(string data) {
        istringstream sin(data);

        TreeNode *pRoot = deserializeDfs(sin);

        return pRoot;
    }


    /**
     * XXX: how to convert the recursive implementation to iterative?
     * Construct the STACK FRAME manually!
     * 1) Add another implicit state: children index to stack frame
     * 2) Or we can just use multilevel pointers of tree nodes
     *
     */
    TreeNode* deserializeIterative(string data) {
        istringstream sin(data);

        TreeNode *pNode = _getNode(sin);
        TreeNode *pRoot = pNode;
        stack<pair<TreeNode*, int>> frontier; // stack frame: [tree node, children index]
        frontier.push({pNode, 0});
        while (frontier.size()) {
            pNode = frontier.top().first;
            int &index = frontier.top().second;

            if (!pNode) {
                frontier.pop();
                continue;
            }
            if (index == 0) {
                pNode->left = _getNode(sin);
                frontier.push({pNode->left, 0});
            } else if (index == 1) {
                pNode->right = _getNode(sin);
                frontier.push({pNode->right, 0});
            } else if (index == 2) { // index == 1, end of children
                frontier.pop();
            }
            ++index;
        }

        return pRoot;
    }
};

/**
 *
 * Postorder serialize and deserialize.
 *
 * Postorder is recursively visit left, right then current node,
 * while preorder is recursively visit node, left then right.
 *
 * 1) So if the serialized string of postorder is reversed, the tree
 * can be deserialized in a similar way to preorder traversal:
 *    visit node, right then left!
 *
 * 2) Can we deserialize without reversing the input string?
 *
 */
class CodecDfsPostorder {
public:
    string serialize(TreeNode *root) {
        const string &output = serializeRecursive(root);
        cout << "postorder serialized: " << output << endl;

        return output;
    }

    void serializeDfs(const TreeNode *pNode, ostringstream &sout) {
        if (!pNode) {
            sout << "#,";
        } else {
            serializeDfs(pNode->left, sout); // left, right, node
            serializeDfs(pNode->right, sout);
            sout << pNode->val << ",";
        }
    }

    string serializeRecursive(TreeNode *root) {
        ostringstream sout;
        serializeDfs(root, sout);

        string output = sout.str();
        trimTrailing(output);

        return output;
    }

    TreeNode* deserialize(string data) {
        TreeNode *pRoot = deserializeRecursiveLikePreorder(data);

        return pRoot;
    }

    TreeNode* deserializeDfs(istringstream &sin) {
        TreeNode *pNode = _getNode(sin);
        if (pNode) {
            pNode->right = deserializeDfs(sin);
            pNode->left = deserializeDfs(sin);
        }
        return pNode;
    }

    TreeNode* deserializeRecursiveLikePreorder(string data) {
        std::reverse(data.begin(), data.end());
        istringstream sin(data);

        return deserializeDfs(sin);
    }
};

class CodecDfsInorder {
public:

    // TODO: implementation
    string serialize(TreeNode *root) {
        //string output = serializeIterative(root);
        string output = serializeRecursive(root);
        //trimTrailing(output);

        cout << "inorder serialized: " << output << endl;
        return output;
    }

    void serializeDfs(TreeNode *root, ostringstream &sout) {
        if (!root) {
            //sout << "#,";
            return;
        }
        sout << "(";
        if (root->left) {
            serializeDfs(root->left, sout);
            //sout << " ";
        }
        sout << root->val;
        if (root->right) {
            serializeDfs(root->right, sout);
            //sout << " ";
        }
        sout << ")";
    }

    string serializeRecursive(TreeNode *root) {
        ostringstream sout;
        serializeDfs(root, sout);

        return sout.str();
    }

    string serializeIterative(TreeNode *root) {
    }

    TreeNode* deserialize(string data) {
        TreeNode *root = deserializeRecursive(data);
        //TreeNode *root = deserializeIterative(data);

        return root;
    }

    TreeNode* deserializeDfs(istringstream &sin) {
        TreeNode *pRoot = _getNode(sin);

        if (pRoot) {
            pRoot->left = deserializeDfs(sin);
            pRoot->right = deserializeDfs(sin);
        }

        return pRoot;
    }

    TreeNode* deserializeRecursive(string data) {
        istringstream sin(data);

        TreeNode *pRoot = deserializeDfs(sin);

        return pRoot;
    }


    /**
     * XXX: how to convert the recursive implementation to iterative?
     * Construct the STACK FRAME manually!
     * 1) Add another implicit state: children index to stack frame
     * 2) Or we can just use multilevel pointers of tree nodes
     *
     */
    TreeNode* deserializeIterative(string data) {
        istringstream sin(data);

        TreeNode *pNode = _getNode(sin);
        TreeNode *pRoot = pNode;
        stack<pair<TreeNode*, int>> frontier; // stack frame: [tree node, children index]
        frontier.push({pNode, 0});
        while (frontier.size()) {
            pNode = frontier.top().first;
            int &index = frontier.top().second;

            if (!pNode) {
                frontier.pop();
                continue;
            }
            if (index == 0) {
                pNode->left = _getNode(sin);
                frontier.push({pNode->left, 0});
            } else if (index == 1) {
                pNode->right = _getNode(sin);
                frontier.push({pNode->right, 0});
            } else if (index == 2) { // index == 1, end of children
                frontier.pop();
            }
            ++index;
        }

        return pRoot;
    }
};



using Codec = CodecBfs;
