# Gainsight NBA plugin

Gainsight NBA is a plugin for Claude that helps a CSM decide what to do next for the accounts in their book, and drafts the email to do it. "NBA" is next best action.

Once installed, you work with it inside Claude. You give it a goal, for example "users who haven't logged in for 30 days." It finds the accounts where that goal came up, checks usage and account history, and writes one short, personal email per user in your customer's tone. You review every draft. Nothing goes to a customer unless you approve it.

Adoption is the first use case. Onboarding and renewal are planned.

## What the plugin adds to Claude

| Part | What it does |
| --- | --- |
| A skill, `nba-agent` | Runs the whole flow. You start it by saying "start the NBA agent." |
| A command, `/gainsight-nba:status` | Shows what's connected and set up, and whether sending is available. |
| A safety check (hook) | Runs before a Gmail send, reply, or forward and blocks any recipient except you, until you turn sending on. |

It doesn't run in the background. It acts only when you start it, and it uses the tools you've already connected to Claude.

## What you need

- Claude Code, or the Code tab in the Claude desktop app.
- A connection to your customer success platform (Gainsight CS in the example setup).
- Optional: a connection to Staircase AI for account health and conversation history.
- Optional: a mail connector so approved drafts land in your drafts folder. Gmail has a built-in adapter. Any other mail tool that can create drafts works too, as drafts only, with no send.
- Two or three real emails from your customer, so the agent can match their tone. You give these once.

## Get started

1. Install the plugin.

   ```
   /plugin marketplace add gs-vjmallya/gainsight-nba-agent
   /plugin install gainsight-nba@gainsight-nba-agent
   ```

2. When you install, Claude asks for two settings:
   - **Gainsight CS MCP server URL.** Each Gainsight tenant has its own, for example `https://<tenant>.gainsightcloud.com/v1/ds-mcp/mcp`. If you've already added Gainsight CS as a connector in Claude, use the same address.
   - **Staircase AI MCP server URL.** Pre-filled. Leave it unless your Staircase account uses a different address.
3. Connect mail (Gmail, for example) if you want drafts in your inbox. Claude may ask you to sign in to each server.
4. Say **start the NBA agent**.

The first time, it asks for what it needs: your customer's name, sample emails, product docs, where your adoption data lives, and your send limits. It saves your answers, so you answer once.

## Testing in a Claude Desktop chat

Desktop chat can load the plugin from a zip. Remove any older copy first, upload the new zip, and start a new chat.

- **The send check does not run in Desktop chat.** Hooks only run in Claude Code. Sending is off by default (`send_enabled: false`) and the skill will not send, but nothing outside the skill enforces it. Use Approve to Gmail draft and review the draft in Gmail. Do not turn sending on in a test.
- **Settings are not saved to files in chat.** The agent cannot write to project knowledge. At the end of setup it gives you the setup files (config, tone, knowledge) as artifacts. Whether a new chat finds them again is still being tested.
- **Use a Claude Project.** Create a Project in Claude, add the setup files to its project knowledge, and start every NBA agent chat inside that Project. Chats in the same Project can read those files, so a new chat skips setup. A chat outside the Project starts setup again. After a run, the agent updates the config with the last goal and counts. Save the updated file to project knowledge again, or the next chat will not see it.
- **Not tested:** that the plugin loads in a chat inside a Project, and that the agent reads the project files there. Tell us what you see.
- **Contact fields come from one tenant.** Field names such as `role0__gc` and `License_Type__gc` were checked on one tenant. Another tenant may name them differently.

Tested so far: the full flow on a real tenant from Claude Code, and the approve flow on fixture data. Not tested yet: Gmail draft creation from Desktop, how the visuals render in Desktop, the health band color, and sending.

## Example prompts

You don't need slash commands to run it. Describe what you want:

- "Start the NBA agent."
- "Set up the NBA agent for Acme."
- "Draft emails to the users in my accounts who haven't logged in for 30 days."
- "Run the NBA agent on my book for low feature adoption."
- `/gainsight-nba:status` shows what's connected and set up.

## Verify, update, and uninstall

- **Verify:** `/plugin` lists `gainsight-nba`. `/gainsight-nba:status` shows your setup.
- **Change a server URL:** `/plugin`, then manage, pick `gainsight-nba`, and choose Configure options. To set them from a terminal, run `claude plugin install gainsight-nba@gainsight-nba-agent --config cs_server_url=<your URL>`.
- **Update:** `/plugin marketplace update gainsight-nba-agent`, then `/plugin update gainsight-nba@gainsight-nba-agent`.
- **Uninstall:** `/plugin uninstall gainsight-nba@gainsight-nba-agent`. Then `/plugin marketplace remove gainsight-nba-agent` if you no longer need the marketplace. Your `.nba-agent/` folder stays, so delete it yourself if you want your settings gone.

## What a run looks like

1. **Check.** It confirms your setup and which tools are connected.
2. **Goal.** You say what to track in plain words. It repeats back the metric, threshold, and time window. You confirm. If you're not sure what to track, it scans your book for common adoption themes and suggests goals.
3. **Find accounts.** It looks for accounts that have talked about that goal in success plans, goals, timeline notes, and conversations. It shows what it found, with the source and date.
4. **Draft.** It checks usage, pulls account context, matches each user to a feature or action from your product docs, and writes 2 or 3 sample emails first. You confirm the tone, then it drafts the rest.
5. **Review.** You see a row of counts (accounts in your book, accounts with the goal, contacts matched, drafts ready, skipped), the queue, and the first draft with the facts it rests on. No click is needed.
6. **Approve.** Approve, edit, or reject each draft one by one. At the end the agent asks once whether to create all approved drafts in your mail tool, or show them for you to copy.
7. **Summary.** You get a final dashboard: how many drafts were approved, how many you edited, and why the rest were skipped.

Every claim in an email comes from something the agent looked up, and each draft lists those facts. Anything the agent inferred is marked.

## Sending

- **Approve** marks a draft approved. At the end you choose to create all approved drafts in your mail tool, or copy them. You send from your mail tool. This is the default.
- **Approve & send** sends for you after you confirm a list of recipients. It's off until you turn it on. To turn it on, open `.nba-agent/config.md` and set `send_enabled: true` yourself. The agent never changes this value.
- **Test send** sends one draft to your own address so you can see how it looks. It only ever goes to you.
- Approve & send needs the plugin install and Gmail. With any other mail tool, the agent creates drafts only. A tool without an adapter is matched at the start and you confirm it once.
- It skips contacts who opted out, have no email, or were contacted recently, and it stays inside your quiet hours and daily limit.

## Your settings

The agent keeps your setup in a `.nba-agent/` folder in your working directory:

| File | What it holds |
| --- | --- |
| `config.md` | Who you are, which tools answer which question, send limits, opt-out source |
| `style.md` | Your customer's tone |
| `knowledge.md` | The features and actions it can recommend |
| `rules.md` | Rules every email must follow (optional) |
| `ledger.jsonl` | A log of drafts and sends (optional) |

Every setting is explained in [docs/configuration.md](docs/configuration.md). Edit these files any time. If you use Claude on the web or the desktop chat, which can't write files, the agent gives you each file to save in your project instead.

## Your data

**What it reads.** Accounts in your book, contacts (name, email, role, opt-out status), goals and success plans, usage and scorecard measures, and account health and conversation themes. It reads only what it needs for the accounts you're working on.

**What it sends.** What it reads passes through Claude as part of your conversation, so your organization's Claude data terms apply. Drafts go to your mail tool only after you approve them and confirm the batch. The plugin itself makes no network calls. During setup, it fetches the product-doc links you give it.

**What it changes.** It never writes to your customer success platform or Staircase. It writes drafts, files in `.nba-agent/`, and, when you turn sending on, the emails you approve.

**What runs on your machine.** One check, `hooks/send-guard.sh`, runs before a Gmail send, reply, or forward. While `send_enabled` is off, it blocks any recipient except you. It does not change any permission settings.

**What stays on your machine.** Your `.nba-agent/` files and the ledger.

## If something isn't working

Run `/gainsight-nba:status`. It shows:
- which tools are connected,
- which setup files exist and which are missing,
- whether sending is available right now, and why.

Common cases:
- **"A required tool isn't connected."** Connect the tool it names, then say start the NBA agent again.
- **A server shows as failed with "URL is unset or invalid."** Open `/plugin`, choose Configure options for `gainsight-nba`, and enter the server address.
- **No mail buttons.** No mail tool is set up. Drafts show in chat so you can copy them.
- **Approve & send is greyed out.** Sending is off, or the plugin isn't installed through the marketplace. The status command says which.
- **Every row says "context not available."** Staircase isn't connected. Drafts rely on usage and your product docs only.
- **Funnel shows text, not tiles.** Your surface can't draw widgets. The numbers are the same.

## Related

- To change tone, rules, or product knowledge, edit the files in `.nba-agent/`.
- Plugin structure and how to add a use case: see `skills/nba-agent/reference/`.
