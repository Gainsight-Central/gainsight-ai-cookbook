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

- The Claude desktop app (chat or the Code tab), or Claude Code.
- A connection to your customer success platform (Gainsight CS in the example setup).
- Optional: a connection to Staircase AI for account health and conversation history.
- Optional: a mail connector so approved drafts land in your drafts folder. Gmail has a built-in adapter. Any other mail tool that can create drafts works too, as drafts only, with no send.
- One or two emails you wrote to a customer, your own words only and not the thread, so the agent can match your tone. You give these once.

## Get started

1. Download the plugin zip: [gainsight-nba-0.1.37.zip](https://github.com/Gainsight-Central/gainsight-ai-cookbook/raw/main/docs/downloads/gainsight-nba-0.1.37.zip). Marketplace install is planned. Until then the zip is the only way to install.

2. Install it. Open Settings, then Plugins, in the Claude desktop app. In Claude Code, `/plugin` opens the same page. Click **Add**, then **Upload plugin**, and choose the zip.

   If you installed an older copy, remove it first. An old copy can be reused from cache. Start a new chat after you install.

3. If Claude asks for settings, enter them:
   - **Gainsight CS MCP server URL.** Each Gainsight tenant has its own, for example `https://<tenant>.gainsightcloud.com/v1/ds-mcp/mcp`. If you've already added Gainsight CS as a connector in Claude, use the same address.
   - **Staircase AI MCP server URL.** Pre-filled. Leave it unless your Staircase account uses a different address.
4. Connect mail (Gmail, for example) if you want drafts in your inbox. Claude may ask you to sign in to each server.
5. Say **start the NBA agent**.

The first time, it asks for what it needs: your customer's name, sample emails, product docs, where your adoption data lives, and your send limits. It saves your answers, so you answer once.

## Using the plugin in Claude desktop chat

Chat can't write files or run the send check, so a few things work differently from Claude Code.

- **Sending stays off.** The send check does not run in chat. Sending is off by default (`send_enabled: false`), and the skill will not send. Use Approve to create Gmail drafts, then review and send from Gmail. Leave sending off in chat.
- **Use a Claude Project.** Chat can't save your settings to files. At the end of setup, the agent gives you the setup files (config, tone, knowledge) to save. Create a Project in Claude, add those files to its project knowledge, and start every NBA agent chat inside that Project. Chats in the Project read the files, so a new chat skips setup. A chat outside the Project starts setup again.
- **Save the updated config.** After a run, the agent updates the config with the last goal and counts. Save the updated file to project knowledge again, or the next chat won't see it.
- **If the opening screen doesn't draw,** type your goal in the message box.
- **If drafts don't show up in Gmail,** choose the copyable list when the agent asks how to hand off approved drafts.
- **Contact field names can differ by tenant.** The agent looks first for fields such as `role0__gc` and `License_Type__gc`. If your tenant names them differently, it finds them from your object metadata.

## Example prompts

You don't need slash commands to run it. Describe what you want:

- "Start the NBA agent."
- "Set up the NBA agent for Acme."
- "Draft emails to the users in my accounts who haven't logged in for 30 days."
- "Run the NBA agent on my book for low feature adoption."
- `/gainsight-nba:status` shows what's connected and set up.

## Verify, update, and uninstall

- **Verify:** the plugin shows under Settings, then Plugins, or in `/plugin` in Claude Code. `/gainsight-nba:status` shows your setup.
- **Change a server URL:** open Settings, then Plugins (or `/plugin` in Claude Code), pick the plugin, and choose Configure options.
- **Update:** download the new zip, remove the old copy, and install the new one as in Get started. Start a new chat.
- **Uninstall:** remove the plugin from Settings, then Plugins. Your `.nba-agent/` folder stays, so delete it yourself if you want your settings gone.

## What a run looks like

1. **Check.** It confirms your setup, which tools are connected, and who is running it. If you name another CSM, it runs for that CSM.
2. **Ready screen.** A banner shows what is connected and that sending is off, with goal cards to click. You can also type your own goal. Where the visual can't draw, you get a short text prompt.
3. **Goal.** You say what to track in plain words. It checks the goal against what your data can measure. If the data can't answer it, it offers the closest options and asks. For example, a tenant with no login metric may offer each contact's last-seen date, and the agent says that is a likely login date, not a confirmed one. It then repeats back the metric, threshold, and time window, and you confirm. If you're not sure what to track, it scans your book for common adoption themes and suggests goals.
4. **Book.** It tells you which accounts it will use, for example "27 active accounts through your CSM field," and asks you to confirm.
5. **Find accounts.** It looks for accounts that have talked about that goal in success plans, goals, timeline notes, and conversations. It shows what it found, with the source and date, and asks whether to continue.
6. **Draft.** It checks usage, pulls account context, and matches each user to a feature or action from your product docs. For more than 5 drafts, it first shows one tone question with three short previews. Then it drafts the rest.
7. **Review.** You see a row of counts (accounts in your book, accounts with the goal, contacts matched, drafts ready, skipped), then a review widget of up to 10 drafts with the first draft open and the facts it rests on. No click is needed to reach the first email. Press Send decisions to record your choices and see the next group.
8. **Approve.** Approve, edit, reject, or skip each draft. Nothing is written until you finish. The agent then asks once whether to create all approved drafts in your mail tool, show them for you to copy, or not now.
9. **Summary.** You get a final dashboard: how many drafts were approved, how many you edited, and why the rest were skipped. The agent saves the run and asks what to do next.

Every claim in an email comes from something the agent looked up, and each draft lists those facts. Anything the agent inferred is marked.

## Sending

- **Approve** marks a draft approved. At the end you choose to create all approved drafts in your mail tool, or copy them. You send from your mail tool. This is the default.
- **Approve & send** sends for you after you confirm a list of recipients. It's off until you turn it on. To turn it on, open `.nba-agent/config.md` and set `send_enabled: true` yourself. The agent never changes this value.
- **Test send** sends one draft to your own address so you can see how it looks. It only ever goes to you.
- Approve & send needs the send check, which does not run in the desktop chat. `/gainsight-nba:status` shows whether it is active. Leave sending off unless it says the check is active. With any other mail tool, the agent creates drafts only. A tool without an adapter is matched at the start and you confirm it once.
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
- **Approve & send is greyed out.** Sending is off, or the send check is not active (it does not run in the desktop chat). The status command says which.
- **Every row says "context not available."** Staircase isn't connected. Drafts rely on usage and your product docs only.
- **Funnel shows text, not tiles.** Your surface can't draw widgets. The numbers are the same.

Still stuck? Email support@gainsight.com. Include the output of `/gainsight-nba:status` and the plugin version.

## Related

- To change tone, rules, or product knowledge, edit the files in `.nba-agent/`.
- Plugin structure and how to add a use case: see `skills/nba-agent/reference/`.
