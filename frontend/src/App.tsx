import { useState } from "react";

const assignees = [
  { name: "Asha Rao", count: 2, initials: "AR", color: "lavender" },
  { name: "Vikram Shah", count: 3, initials: "VS", color: "mint" },
  { name: "Meera Iyer", count: 1, initials: "MI", color: "peach" },
  { name: "Unassigned", count: 1, initials: "—", color: "gray" },
];

const blockers = [
  {
    key: "TCL-388",
    title: "Import supplier price list",
    owner: "Vikram Shah",
    initials: "VS",
    since: "Oct 27",
    points: "5 pts",
    reason: "Waiting for supplier file format confirmation",
  },
  {
    key: "TCL-401",
    title: "Approval workflow for cost changes",
    owner: "Meera Iyer",
    initials: "MI",
    since: "Oct 29",
    points: "—",
    reason: "Reason not available",
  },
];

function Trend({ children }: { children: string }) {
  return <span className="trend">{children}</span>;
}

function App() {
  const [showPreviewNotice, setShowPreviewNotice] = useState(true);

  return (
    <div className="app-shell">
      <aside className="sidebar">
        <a className="brand" href="#" aria-label="Costing Workbench home">
          <span className="brand-mark" aria-hidden="true">
            <i />
            <i />
            <i />
          </span>
          <span>
            <strong>Costing</strong>
            <small>WORKBENCH</small>
          </span>
        </a>

        <div className="workspace-label">WORKSPACE</div>
        <div className="project-switcher">
          <span className="project-avatar">C</span>
          <span className="project-copy">
            <strong>Costing project</strong>
            <small>TCL · Jira Cloud</small>
          </span>
          <span className="chevron" aria-hidden="true">⌄</span>
        </div>

        <nav className="primary-nav" aria-label="Main navigation">
          <a className="nav-item active" href="#overview" aria-current="page">
            <span className="nav-icon" aria-hidden="true">◫</span>
            Overview
          </a>
          <button className="nav-item muted" type="button" disabled>
            <span className="nav-icon" aria-hidden="true">▤</span>
            Reports
            <span className="nav-soon">Soon</span>
          </button>
          <button className="nav-item muted" type="button" disabled>
            <span className="nav-icon" aria-hidden="true">⚙</span>
            Settings
          </button>
        </nav>

        <div className="sidebar-bottom">
          <div className="help-card">
            <span className="help-icon" aria-hidden="true">?</span>
            <div>
              <strong>Need a hand?</strong>
              <span>View setup guide</span>
            </div>
            <span className="chevron" aria-hidden="true">↗</span>
          </div>
          <div className="profile">
            <span className="profile-avatar">SM</span>
            <span className="profile-copy">
              <strong>Scrum Master</strong>
              <small>Project reviewer</small>
            </span>
            <span className="chevron" aria-hidden="true">···</span>
          </div>
        </div>
      </aside>

      <main className="main-content" id="overview">
        <header className="topbar">
          <div className="breadcrumb">
            <span>Workspace</span>
            <b>/</b>
            <strong>Overview</strong>
          </div>
          <div className="topbar-actions">
            <span className="preview-chip"><span /> Preview data</span>
            <button
              className="button button-primary"
              type="button"
              disabled
              title="Report generation is unavailable until the backend is connected."
            >
              <span aria-hidden="true">＋</span>
              Generate report
            </button>
            <button className="icon-button" type="button" aria-label="Notifications">
              ♧
              <span className="notification-dot" />
            </button>
          </div>
        </header>

        <div className="content-wrap">
          <section className="page-heading">
            <div>
              <div className="eyebrow">MONDAY, NOVEMBER 2, 2026</div>
              <h1>Weekly delivery</h1>
              <p>Here’s the latest snapshot of your team’s progress and outlook.</p>
            </div>
            <button className="date-button" type="button" disabled>
              <span aria-hidden="true">▦</span>
              Oct 26 – Oct 30, 2026
              <span className="chevron" aria-hidden="true">⌄</span>
            </button>
          </section>

          {showPreviewNotice && (
            <div className="preview-banner" role="note">
              <span className="banner-icon" aria-hidden="true">i</span>
              <p><strong>Preview only</strong> — all figures below are fictional sample data. This UI is not connected to Jira or a report service.</p>
              <button type="button" aria-label="Dismiss preview notice" onClick={() => setShowPreviewNotice(false)}>×</button>
            </div>
          )}

          <section className="stats-grid" aria-label="Weekly report summary">
            <article className="stat-card">
              <div className="stat-top">
                <span className="stat-label">Stories completed</span>
                <span className="stat-icon icon-lavender" aria-hidden="true">✓</span>
              </div>
              <div className="stat-value">7</div>
              <div className="stat-foot"><Trend>↑ 2</Trend><span>vs. previous week</span></div>
            </article>
            <article className="stat-card">
              <div className="stat-top">
                <span className="stat-label">Currently blocked</span>
                <span className="stat-icon icon-amber" aria-hidden="true">Ⅱ</span>
              </div>
              <div className="stat-value">2</div>
              <div className="stat-foot"><span className="foot-neutral">Needs attention</span></div>
            </article>
            <article className="stat-card">
              <div className="stat-top">
                <span className="stat-label">Average velocity</span>
                <span className="stat-icon icon-blue" aria-hidden="true">↗</span>
              </div>
              <div className="stat-value">31<span className="stat-unit">pts</span></div>
              <div className="stat-foot"><span>Last 3 completed sprints</span></div>
            </article>
            <article className="stat-card">
              <div className="stat-top">
                <span className="stat-label">Open Priority 1 defects</span>
                <span className="stat-icon icon-red" aria-hidden="true">!</span>
              </div>
              <div className="stat-value">1</div>
              <div className="stat-foot"><span className="foot-alert">Review required</span></div>
            </article>
          </section>

          <section className="dashboard-grid">
            <article className="panel completed-panel">
              <div className="panel-heading">
                <div>
                  <h2>Completed stories</h2>
                  <p>By assignee <span className="scope-tag">Ready for deployment</span></p>
                </div>
                <button className="text-button" type="button" disabled>View report <span aria-hidden="true">↗</span></button>
              </div>
              <div className="assignee-list">
                {assignees.map((assignee) => (
                  <div className="assignee-row" key={assignee.name}>
                    <span className={`avatar avatar-${assignee.color}`}>{assignee.initials}</span>
                    <span className="assignee-name">{assignee.name}</span>
                    <span className="bar-track" aria-hidden="true">
                      <span style={{ width: `${(assignee.count / 3) * 100}%` }} />
                    </span>
                    <strong className="assignee-count">{assignee.count}</strong>
                  </div>
                ))}
              </div>
              <div className="panel-total">
                <span>Team total</span>
                <strong>7 <small>stories</small></strong>
              </div>
            </article>

            <article className="panel forecast-panel">
              <div className="panel-heading">
                <div>
                  <h2>Quarter outlook</h2>
                  <p>Capacity based on recent velocity</p>
                </div>
                <span className="provisional-tag">PROVISIONAL</span>
              </div>
              <div className="forecast-capacity">
                <div>
                  <span className="capacity-label">Estimated point capacity</span>
                  <strong>124 <small>pts</small></strong>
                </div>
                <div className="capacity-formula">31 pts × 4 sprints</div>
              </div>
              <div className="forecast-progress-label">
                <span>Backlog stories that fit</span>
                <strong>15 <small>of 18</small></strong>
              </div>
              <div className="progress-track" role="img" aria-label="15 of 18 backlog stories fit within estimated capacity">
                <span />
              </div>
              <div className="forecast-foot">
                <span>Quarter ends Dec 31, 2026</span>
                <span>18 stories · 140 pts</span>
              </div>
              <div className="forecast-note">
                <span aria-hidden="true">i</span>
                Fits within capacity does not guarantee delivery.
              </div>
            </article>
          </section>

          <section className="dashboard-grid lower-grid">
            <article className="panel blockers-panel">
              <div className="panel-heading">
                <div>
                  <h2>Current blockers <span className="count-pill">2</span></h2>
                  <p>Stories needing a follow-up</p>
                </div>
                <button className="text-button" type="button" disabled>View all <span aria-hidden="true">→</span></button>
              </div>
              <div className="blocker-list">
                {blockers.map((blocker) => (
                  <div className="blocker-row" key={blocker.key}>
                    <div className="blocker-main">
                      <div className="blocker-title-line">
                        <a href={`#${blocker.key}`}>{blocker.title}</a>
                        <span className="issue-key">{blocker.key}</span>
                      </div>
                      <div className="blocker-reason">{blocker.reason}</div>
                      <div className="blocker-meta">
                        <span className={`avatar avatar-${blocker.initials === "VS" ? "mint" : "peach"}`}>{blocker.initials}</span>
                        <span>{blocker.owner}</span>
                        <span className="meta-separator">·</span>
                        <span>Blocked {blocker.since}</span>
                      </div>
                    </div>
                    <span className="points-tag">{blocker.points}</span>
                  </div>
                ))}
              </div>
            </article>

            <article className="panel defect-panel">
              <div className="panel-heading">
                <div>
                  <h2>Priority 1 defect</h2>
                  <p>Open and requiring attention</p>
                </div>
                <span className="critical-label"><span /> Critical</span>
              </div>
              <div className="defect-content">
                <span className="defect-key">TCL-412</span>
                <a className="defect-title" href="#TCL-412">Cost roll-up returns wrong total for multi-currency BOM</a>
                <div className="defect-meta">
                  <span className="status-dot" />
                  <span>In Progress</span>
                  <span className="meta-separator">·</span>
                  <span>Created Oct 28</span>
                </div>
              </div>
              <div className="defect-footer">
                <span>Assignee</span>
                <span className="defect-owner"><span className="avatar avatar-lavender">AR</span>Asha Rao</span>
              </div>
            </article>
          </section>

          <footer className="page-footer">
            <span>Reporting period: Oct 26 – Oct 30, 2026 (IST)</span>
            <span>Draft for Scrum Master review</span>
          </footer>
        </div>
      </main>
    </div>
  );
}

export default App;