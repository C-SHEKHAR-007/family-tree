## Family Tree Data Model — System Design & Implementation Reference

---

# 1. Overview

This document defines the complete data modeling strategy for the Family Tree system.

The goal is to support:

* Hierarchical family relationships
* Multi-generational trees
* Parent-child relationships
* Spousal relationships
* Sibling derivation
* Future scalability for complex kinship queries

The design is relational and implemented using SQLAlchemy ORM.

---

# 2. Design Philosophy

The family tree is modeled using an  **Adjacency List Pattern** .

Each person:

* Can have a parent reference
* Can have multiple children
* Can belong to one family tree

This allows:

* Recursive queries
* Efficient parent-child traversal
* Expandability

---

# 3. Core Entities

---

# 3.1 User

Represents an authenticated system user.

### Purpose

* Authentication
* Authorization
* Ownership of family tree

### Fields

* `id` (UUID, PK)
* `email` (unique)
* `password_hash`
* `role`
* `created_at`
* `updated_at`

### Relationships

* One user can own one or more family trees.

---

# 3.2 FamilyTree

Represents a root container for a family hierarchy.

### Purpose

* Logical grouping of related persons
* Multi-tenant support (each user can have their own tree)

### Fields

* `id` (UUID, PK)
* `name`
* `owner_id` (FK → User.id)
* `created_at`
* `updated_at`

### Relationships

* One FamilyTree has many Persons
* One User owns many FamilyTrees

---

# 3.3 Person

Represents an individual in the family tree.

This is the core hierarchical node.

---

## 3.3.1 Core Fields

* `id` (UUID, PK)
* `first_name`
* `last_name`
* `gender`
* `date_of_birth`
* `date_of_death`
* `family_tree_id` (FK → FamilyTree.id)
* `parent_id` (FK → Person.id, nullable)
* `spouse_id` (FK → Person.id, nullable)
* `created_at`
* `updated_at`

---

# 4. Relationship Modeling Strategy

---

# 4.1 Parent-Child Relationship

Modeled using:

<pre class="overflow-visible! px-0!" data-start="2055" data-end="2095"><div class="w-full my-4"><div class=""><div class="relative"><div class="h-full min-h-0 min-w-0"><div class="h-full min-h-0 min-w-0"><div class="border corner-superellipse/1.1 border-token-border-light bg-token-bg-elevated-secondary rounded-3xl"><div class="pointer-events-none absolute inset-x-4 top-12 bottom-4"><div class="pointer-events-none sticky z-40 shrink-0 z-1!"><div class="sticky bg-token-border-light"></div></div></div><div class="pointer-events-none absolute inset-x-px top-0 bottom-96"><div class="pointer-events-none sticky z-40 shrink-0 z-1!"><div class="sticky bg-token-bg-elevated-secondary"></div></div></div><div class="corner-superellipse/1.1 rounded-3xl bg-token-bg-elevated-secondary"><div class="relative z-0 flex max-w-full"><div id="code-block-viewer" dir="ltr" class="q9tKkq_viewer cm-editor z-10 light:cm-light dark:cm-light flex h-full w-full flex-col items-stretch ͼk ͼy"><div class="cm-scroller"><div class="cm-content q9tKkq_readonly"><span>parent_id → references Person.id</span></div></div></div></div></div></div></div></div><div class=""><div class=""></div></div></div></div></div></pre>

This creates:

<pre class="overflow-visible! px-0!" data-start="2112" data-end="2136"><div class="w-full my-4"><div class=""><div class="relative"><div class="h-full min-h-0 min-w-0"><div class="h-full min-h-0 min-w-0"><div class="border corner-superellipse/1.1 border-token-border-light bg-token-bg-elevated-secondary rounded-3xl"><div class="pointer-events-none absolute inset-x-4 top-12 bottom-4"><div class="pointer-events-none sticky z-40 shrink-0 z-1!"><div class="sticky bg-token-border-light"></div></div></div><div class="pointer-events-none absolute inset-x-px top-0 bottom-96"><div class="pointer-events-none sticky z-40 shrink-0 z-1!"><div class="sticky bg-token-bg-elevated-secondary"></div></div></div><div class="corner-superellipse/1.1 rounded-3xl bg-token-bg-elevated-secondary"><div class="relative z-0 flex max-w-full"><div id="code-block-viewer" dir="ltr" class="q9tKkq_viewer cm-editor z-10 light:cm-light dark:cm-light flex h-full w-full flex-col items-stretch ͼk ͼy"><div class="cm-scroller"><div class="cm-content q9tKkq_readonly"><span>Parent</span><br/><span>  ↓</span><br/><span>Child</span></div></div></div></div></div></div></div></div><div class=""><div class=""></div></div></div></div></div></pre>

In SQLAlchemy:

<pre class="overflow-visible! px-0!" data-start="2154" data-end="2237"><div class="w-full my-4"><div class=""><div class="relative"><div class="h-full min-h-0 min-w-0"><div class="h-full min-h-0 min-w-0"><div class="border corner-superellipse/1.1 border-token-border-light bg-token-bg-elevated-secondary rounded-3xl"><div class="pointer-events-none absolute inset-x-4 top-12 bottom-4"><div class="pointer-events-none sticky z-40 shrink-0 z-1!"><div class="sticky bg-token-border-light"></div></div></div><div class="pointer-events-none absolute inset-x-px top-0 bottom-96"><div class="pointer-events-none sticky z-40 shrink-0 z-1!"><div class="sticky bg-token-bg-elevated-secondary"></div></div></div><div class="corner-superellipse/1.1 rounded-3xl bg-token-bg-elevated-secondary"><div class="relative z-0 flex max-w-full"><div id="code-block-viewer" dir="ltr" class="q9tKkq_viewer cm-editor z-10 light:cm-light dark:cm-light flex h-full w-full flex-col items-stretch ͼk ͼy"><div class="cm-scroller"><div class="cm-content q9tKkq_readonly"><span class="ͼt">parent</span><span></span><span class="ͼn">=</span><span></span><span class="ͼt">relationship</span><span>(</span><span class="ͼr">"Person"</span><span>, </span><span class="ͼt">remote_side</span><span class="ͼn">=</span><span>[</span><span class="ͼt">id</span><span>], </span><span class="ͼt">backref</span><span class="ͼn">=</span><span class="ͼr">"children"</span><span>)</span></div></div></div></div></div></div></div></div><div class=""><div class=""></div></div></div></div></div></pre>

This allows:

* `person.children`
* `person.parent`

---

# 4.2 Spousal Relationship

Option 1 (Simple):

<pre class="overflow-visible! px-0!" data-start="2345" data-end="2374"><div class="w-full my-4"><div class=""><div class="relative"><div class="h-full min-h-0 min-w-0"><div class="h-full min-h-0 min-w-0"><div class="border corner-superellipse/1.1 border-token-border-light bg-token-bg-elevated-secondary rounded-3xl"><div class="pointer-events-none absolute inset-x-4 top-12 bottom-4"><div class="pointer-events-none sticky z-40 shrink-0 z-1!"><div class="sticky bg-token-border-light"></div></div></div><div class="pointer-events-none absolute inset-x-px top-0 bottom-96"><div class="pointer-events-none sticky z-40 shrink-0 z-1!"><div class="sticky bg-token-bg-elevated-secondary"></div></div></div><div class="corner-superellipse/1.1 rounded-3xl bg-token-bg-elevated-secondary"><div class="relative z-0 flex max-w-full"><div id="code-block-viewer" dir="ltr" class="q9tKkq_viewer cm-editor z-10 light:cm-light dark:cm-light flex h-full w-full flex-col items-stretch ͼk ͼy"><div class="cm-scroller"><div class="cm-content q9tKkq_readonly"><span>spouse_id → Person.id</span></div></div></div></div></div></div></div></div><div class=""><div class=""></div></div></div></div></div></pre>

Limitations:

* Only one spouse
* Hard to track historical marriages

Option 2 (Recommended for future scalability):

Create separate `Marriage` table.

---

# 4.3 Recommended Marriage Model (Future Upgrade)

## Marriage Table

Fields:

* `id`
* `person1_id`
* `person2_id`
* `married_on`
* `divorced_on`

This allows:

* Multiple marriages
* Historical tracking
* Clean normalization

---

# 5. Data Model Diagram (Conceptual)

<pre class="overflow-visible! px-0!" data-start="2804" data-end="2947"><div class="w-full my-4"><div class=""><div class="relative"><div class="h-full min-h-0 min-w-0"><div class="h-full min-h-0 min-w-0"><div class="border corner-superellipse/1.1 border-token-border-light bg-token-bg-elevated-secondary rounded-3xl"><div class="pointer-events-none absolute inset-x-4 top-12 bottom-4"><div class="pointer-events-none sticky z-40 shrink-0 z-1!"><div class="sticky bg-token-border-light"></div></div></div><div class="pointer-events-none absolute inset-x-px top-0 bottom-96"><div class="pointer-events-none sticky z-40 shrink-0 z-1!"><div class="sticky bg-token-bg-elevated-secondary"></div></div></div><div class="corner-superellipse/1.1 rounded-3xl bg-token-bg-elevated-secondary"><div class="relative z-0 flex max-w-full"><div id="code-block-viewer" dir="ltr" class="q9tKkq_viewer cm-editor z-10 light:cm-light dark:cm-light flex h-full w-full flex-col items-stretch ͼk ͼy"><div class="cm-scroller"><div class="cm-content q9tKkq_readonly"><span>User</span><br/><span> └── FamilyTree</span><br/><span>       └── Person</span><br/><span>             ├── parent_id → Person</span><br/><span>             ├── children</span><br/><span>             └── spouse (optional)</span></div></div></div></div></div></div></div></div><div class=""><div class=""></div></div></div></div></div></pre>

---

# 6. Hierarchical Query Strategy

---

# 6.1 Get Children

<pre class="overflow-visible! px-0!" data-start="3013" data-end="3042"><div class="w-full my-4"><div class=""><div class="relative"><div class="h-full min-h-0 min-w-0"><div class="h-full min-h-0 min-w-0"><div class="border corner-superellipse/1.1 border-token-border-light bg-token-bg-elevated-secondary rounded-3xl"><div class="pointer-events-none absolute inset-x-4 top-12 bottom-4"><div class="pointer-events-none sticky z-40 shrink-0 z-1!"><div class="sticky bg-token-border-light"></div></div></div><div class="pointer-events-none absolute inset-x-px top-0 bottom-96"><div class="pointer-events-none sticky z-40 shrink-0 z-1!"><div class="sticky bg-token-bg-elevated-secondary"></div></div></div><div class="corner-superellipse/1.1 rounded-3xl bg-token-bg-elevated-secondary"><div class="relative z-0 flex max-w-full"><div id="code-block-viewer" dir="ltr" class="q9tKkq_viewer cm-editor z-10 light:cm-light dark:cm-light flex h-full w-full flex-col items-stretch ͼk ͼy"><div class="cm-scroller"><div class="cm-content q9tKkq_readonly"><span class="ͼt">person</span><span class="ͼn">.</span><span>children</span></div></div></div></div></div></div></div></div><div class=""><div class=""></div></div></div></div></div></pre>

---

# 6.2 Get Parent

<pre class="overflow-visible! px-0!" data-start="3067" data-end="3094"><div class="w-full my-4"><div class=""><div class="relative"><div class="h-full min-h-0 min-w-0"><div class="h-full min-h-0 min-w-0"><div class="border corner-superellipse/1.1 border-token-border-light bg-token-bg-elevated-secondary rounded-3xl"><div class="pointer-events-none absolute inset-x-4 top-12 bottom-4"><div class="pointer-events-none sticky z-40 shrink-0 z-1!"><div class="sticky bg-token-border-light"></div></div></div><div class="pointer-events-none absolute inset-x-px top-0 bottom-96"><div class="pointer-events-none sticky z-40 shrink-0 z-1!"><div class="sticky bg-token-bg-elevated-secondary"></div></div></div><div class="corner-superellipse/1.1 rounded-3xl bg-token-bg-elevated-secondary"><div class="relative z-0 flex max-w-full"><div id="code-block-viewer" dir="ltr" class="q9tKkq_viewer cm-editor z-10 light:cm-light dark:cm-light flex h-full w-full flex-col items-stretch ͼk ͼy"><div class="cm-scroller"><div class="cm-content q9tKkq_readonly"><span class="ͼt">person</span><span class="ͼn">.</span><span>parent</span></div></div></div></div></div></div></div></div><div class=""><div class=""></div></div></div></div></div></pre>

---

# 6.3 Get Siblings

Derived, not stored:

<pre class="overflow-visible! px-0!" data-start="3143" data-end="3201"><div class="w-full my-4"><div class=""><div class="relative"><div class="h-full min-h-0 min-w-0"><div class="h-full min-h-0 min-w-0"><div class="border corner-superellipse/1.1 border-token-border-light bg-token-bg-elevated-secondary rounded-3xl"><div class="pointer-events-none absolute inset-x-4 top-12 bottom-4"><div class="pointer-events-none sticky z-40 shrink-0 z-1!"><div class="sticky bg-token-border-light"></div></div></div><div class="pointer-events-none absolute inset-x-px top-0 bottom-96"><div class="pointer-events-none sticky z-40 shrink-0 z-1!"><div class="sticky bg-token-bg-elevated-secondary"></div></div></div><div class="corner-superellipse/1.1 rounded-3xl bg-token-bg-elevated-secondary"><div class="relative z-0 flex max-w-full"><div id="code-block-viewer" dir="ltr" class="q9tKkq_viewer cm-editor z-10 light:cm-light dark:cm-light flex h-full w-full flex-col items-stretch ͼk ͼy"><div class="cm-scroller"><div class="cm-content q9tKkq_readonly"><span>siblings = person.parent.children (excluding self)</span></div></div></div></div></div></div></div></div><div class=""><div class=""></div></div></div></div></div></pre>

---

# 6.4 Get Ancestors (Recursive)

Use recursive CTE:

<pre class="overflow-visible! px-0!" data-start="3261" data-end="3302"><div class="w-full my-4"><div class=""><div class="relative"><div class="h-full min-h-0 min-w-0"><div class="h-full min-h-0 min-w-0"><div class="border corner-superellipse/1.1 border-token-border-light bg-token-bg-elevated-secondary rounded-3xl"><div class="pointer-events-none absolute inset-x-4 top-12 bottom-4"><div class="pointer-events-none sticky z-40 shrink-0 z-1!"><div class="sticky bg-token-border-light"></div></div></div><div class="pointer-events-none absolute inset-x-px top-0 bottom-96"><div class="pointer-events-none sticky z-40 shrink-0 z-1!"><div class="sticky bg-token-bg-elevated-secondary"></div></div></div><div class="corner-superellipse/1.1 rounded-3xl bg-token-bg-elevated-secondary"><div class="relative z-0 flex max-w-full"><div id="code-block-viewer" dir="ltr" class="q9tKkq_viewer cm-editor z-10 light:cm-light dark:cm-light flex h-full w-full flex-col items-stretch ͼk ͼy"><div class="cm-scroller"><div class="cm-content q9tKkq_readonly"><span>WITH RECURSIVE ancestors AS (...)</span></div></div></div></div></div></div></div></div><div class=""><div class=""></div></div></div></div></div></pre>

Or iterative approach in Python.

---

# 6.5 Get Descendants

Recursive traversal from root node.

---

# 7. Multi-Tenancy Design

Each Person belongs to:

<pre class="overflow-visible! px-0!" data-start="3460" data-end="3482"><div class="w-full my-4"><div class=""><div class="relative"><div class="h-full min-h-0 min-w-0"><div class="h-full min-h-0 min-w-0"><div class="border corner-superellipse/1.1 border-token-border-light bg-token-bg-elevated-secondary rounded-3xl"><div class="pointer-events-none absolute inset-x-4 top-12 bottom-4"><div class="pointer-events-none sticky z-40 shrink-0 z-1!"><div class="sticky bg-token-border-light"></div></div></div><div class="pointer-events-none absolute inset-x-px top-0 bottom-96"><div class="pointer-events-none sticky z-40 shrink-0 z-1!"><div class="sticky bg-token-bg-elevated-secondary"></div></div></div><div class="corner-superellipse/1.1 rounded-3xl bg-token-bg-elevated-secondary"><div class="relative z-0 flex max-w-full"><div id="code-block-viewer" dir="ltr" class="q9tKkq_viewer cm-editor z-10 light:cm-light dark:cm-light flex h-full w-full flex-col items-stretch ͼk ͼy"><div class="cm-scroller"><div class="cm-content q9tKkq_readonly"><span>family_tree_id</span></div></div></div></div></div></div></div></div><div class=""><div class=""></div></div></div></div></div></pre>

This ensures:

* One user cannot access another user's tree
* Query always filtered by family_tree_id

Example filter:

<pre class="overflow-visible! px-0!" data-start="3604" data-end="3678"><div class="w-full my-4"><div class=""><div class="relative"><div class="h-full min-h-0 min-w-0"><div class="h-full min-h-0 min-w-0"><div class="border corner-superellipse/1.1 border-token-border-light bg-token-bg-elevated-secondary rounded-3xl"><div class="pointer-events-none absolute inset-x-4 top-12 bottom-4"><div class="pointer-events-none sticky z-40 shrink-0 z-1!"><div class="sticky bg-token-border-light"></div></div></div><div class="pointer-events-none absolute inset-x-px top-0 bottom-96"><div class="pointer-events-none sticky z-40 shrink-0 z-1!"><div class="sticky bg-token-bg-elevated-secondary"></div></div></div><div class="corner-superellipse/1.1 rounded-3xl bg-token-bg-elevated-secondary"><div class="relative z-0 flex max-w-full"><div id="code-block-viewer" dir="ltr" class="q9tKkq_viewer cm-editor z-10 light:cm-light dark:cm-light flex h-full w-full flex-col items-stretch ͼk ͼy"><div class="cm-scroller"><div class="cm-content q9tKkq_readonly"><span class="ͼt">db</span><span class="ͼn">.</span><span>query(</span><span class="ͼt">Person</span><span>)</span><br/><span>  .</span><span class="ͼt">filter</span><span>(</span><span class="ͼt">Person</span><span class="ͼn">.</span><span>family_tree_id </span><span class="ͼn">==</span><span></span><span class="ͼt">tree_id</span><span>)</span></div></div></div></div></div></div></div></div><div class=""><div class=""></div></div></div></div></div></pre>

---

# 8. Database Constraints

---

## 8.1 Required Constraints

* email UNIQUE
* parent_id FK constraint
* family_tree_id NOT NULL
* owner_id NOT NULL

---

## 8.2 Optional Constraints

* Prevent circular parent relationships (application-level validation)
* Prevent self-parenting
* Prevent spouse self-reference

---

# 9. Indexing Strategy

For performance:

Add indexes on:

* `family_tree_id`
* `parent_id`
* `owner_id`
* `email`

This improves:

* Hierarchical queries
* Tree filtering
* Login performance

---

# 10. Data Integrity Rules

---

## 10.1 Parent Rules

* A person cannot be their own parent
* Parent must belong to same family_tree
* No circular references

---

## 10.2 Spouse Rules

* Cannot marry self
* Spouse must belong to same family_tree

---

## 10.3 Deletion Rules

Option A:

* Cascade delete children

Option B (Recommended):

* Soft delete flag

Add:

<pre class="overflow-visible! px-0!" data-start="4565" data-end="4592"><div class="w-full my-4"><div class=""><div class="relative"><div class="h-full min-h-0 min-w-0"><div class="h-full min-h-0 min-w-0"><div class="border corner-superellipse/1.1 border-token-border-light bg-token-bg-elevated-secondary rounded-3xl"><div class="pointer-events-none absolute inset-x-4 top-12 bottom-4"><div class="pointer-events-none sticky z-40 shrink-0 z-1!"><div class="sticky bg-token-border-light"></div></div></div><div class="pointer-events-none absolute inset-x-px top-0 bottom-96"><div class="pointer-events-none sticky z-40 shrink-0 z-1!"><div class="sticky bg-token-bg-elevated-secondary"></div></div></div><div class="corner-superellipse/1.1 rounded-3xl bg-token-bg-elevated-secondary"><div class="relative z-0 flex max-w-full"><div id="code-block-viewer" dir="ltr" class="q9tKkq_viewer cm-editor z-10 light:cm-light dark:cm-light flex h-full w-full flex-col items-stretch ͼk ͼy"><div class="cm-scroller"><div class="cm-content q9tKkq_readonly"><span>is_active (boolean)</span></div></div></div></div></div></div></div></div><div class=""><div class=""></div></div></div></div></div></pre>

Safer for real-world usage.

---

# 11. Future Relationship Extensions

---

## 11.1 Adopted Relationships

Add:

<pre class="overflow-visible! px-0!" data-start="4708" data-end="4733"><div class="w-full my-4"><div class=""><div class="relative"><div class="h-full min-h-0 min-w-0"><div class="h-full min-h-0 min-w-0"><div class="border corner-superellipse/1.1 border-token-border-light bg-token-bg-elevated-secondary rounded-3xl"><div class="pointer-events-none absolute inset-x-4 top-12 bottom-4"><div class="pointer-events-none sticky z-40 shrink-0 z-1!"><div class="sticky bg-token-border-light"></div></div></div><div class="pointer-events-none absolute inset-x-px top-0 bottom-96"><div class="pointer-events-none sticky z-40 shrink-0 z-1!"><div class="sticky bg-token-bg-elevated-secondary"></div></div></div><div class="corner-superellipse/1.1 rounded-3xl bg-token-bg-elevated-secondary"><div class="relative z-0 flex max-w-full"><div id="code-block-viewer" dir="ltr" class="q9tKkq_viewer cm-editor z-10 light:cm-light dark:cm-light flex h-full w-full flex-col items-stretch ͼk ͼy"><div class="cm-scroller"><div class="cm-content q9tKkq_readonly"><span>relationship_type</span></div></div></div></div></div></div></div></div><div class=""><div class=""></div></div></div></div></div></pre>

Values:

* biological
* adopted
* step

---

## 11.2 Sibling Relationship Table (Optional)

Not necessary because siblings are derived.

---

## 11.3 Extended Family Relations

Future:

* Cousins
* In-laws
* Grandparents
* Lineage depth calculations

All derivable from parent-child graph.

---

# 12. Scalability Considerations

---

## 12.1 Expected Growth

* Thousands of persons per tree
* Multiple trees per user

Adjacency list handles this efficiently.

---

## 12.2 Recursive Depth

Most family trees:

* 4–10 generations

Safe for recursive CTE queries.

---

# 13. Performance Optimization (Future)

* Caching subtree results
* Materialized path pattern (if needed)
* Precomputed lineage depth
* Redis cache layer

---

# 14. Current Implementation Status

| Component          | Status                 |
| ------------------ | ---------------------- |
| User model         | Complete               |
| FamilyTree model   | Partially defined      |
| Person model       | Core structure defined |
| Parent-child logic | Designed               |
| Marriage table     | Planned                |
| Recursive queries  | Planned                |

---

# 15. Comparison of Hierarchical Modeling Approaches

| Pattern           | Used? | Reason                       |
| ----------------- | ----- | ---------------------------- |
| Adjacency List    | ✅    | Simple, flexible             |
| Nested Set        | ❌    | Complex updates              |
| Materialized Path | ⏳    | Possible future optimization |
| Closure Table     | ⏳    | For high-scale graphs        |

Current system uses Adjacency List.

---

# 16. Example Data Flow

Create Tree:

<pre class="overflow-visible! px-0!" data-start="6136" data-end="6168"><div class="w-full my-4"><div class=""><div class="relative"><div class="h-full min-h-0 min-w-0"><div class="h-full min-h-0 min-w-0"><div class="border corner-superellipse/1.1 border-token-border-light bg-token-bg-elevated-secondary rounded-3xl"><div class="pointer-events-none absolute inset-x-4 top-12 bottom-4"><div class="pointer-events-none sticky z-40 shrink-0 z-1!"><div class="sticky bg-token-border-light"></div></div></div><div class="pointer-events-none absolute inset-x-px top-0 bottom-96"><div class="pointer-events-none sticky z-40 shrink-0 z-1!"><div class="sticky bg-token-bg-elevated-secondary"></div></div></div><div class="corner-superellipse/1.1 rounded-3xl bg-token-bg-elevated-secondary"><div class="relative z-0 flex max-w-full"><div id="code-block-viewer" dir="ltr" class="q9tKkq_viewer cm-editor z-10 light:cm-light dark:cm-light flex h-full w-full flex-col items-stretch ͼk ͼy"><div class="cm-scroller"><div class="cm-content q9tKkq_readonly"><span>User → create FamilyTree</span></div></div></div></div></div></div></div></div><div class=""><div class=""></div></div></div></div></div></pre>

Add Root Person:

<pre class="overflow-visible! px-0!" data-start="6188" data-end="6218"><div class="w-full my-4"><div class=""><div class="relative"><div class="h-full min-h-0 min-w-0"><div class="h-full min-h-0 min-w-0"><div class="border corner-superellipse/1.1 border-token-border-light bg-token-bg-elevated-secondary rounded-3xl"><div class="pointer-events-none absolute inset-x-4 top-12 bottom-4"><div class="pointer-events-none sticky z-40 shrink-0 z-1!"><div class="sticky bg-token-border-light"></div></div></div><div class="pointer-events-none absolute inset-x-px top-0 bottom-96"><div class="pointer-events-none sticky z-40 shrink-0 z-1!"><div class="sticky bg-token-bg-elevated-secondary"></div></div></div><div class="corner-superellipse/1.1 rounded-3xl bg-token-bg-elevated-secondary"><div class="relative z-0 flex max-w-full"><div id="code-block-viewer" dir="ltr" class="q9tKkq_viewer cm-editor z-10 light:cm-light dark:cm-light flex h-full w-full flex-col items-stretch ͼk ͼy"><div class="cm-scroller"><div class="cm-content q9tKkq_readonly"><span>Person(parent_id=None)</span></div></div></div></div></div></div></div></div><div class=""><div class=""></div></div></div></div></div></pre>

Add Child:

<pre class="overflow-visible! px-0!" data-start="6232" data-end="6265"><div class="w-full my-4"><div class=""><div class="relative"><div class="h-full min-h-0 min-w-0"><div class="h-full min-h-0 min-w-0"><div class="border corner-superellipse/1.1 border-token-border-light bg-token-bg-elevated-secondary rounded-3xl"><div class="pointer-events-none absolute inset-x-4 top-12 bottom-4"><div class="pointer-events-none sticky z-40 shrink-0 z-1!"><div class="sticky bg-token-border-light"></div></div></div><div class="pointer-events-none absolute inset-x-px top-0 bottom-96"><div class="pointer-events-none sticky z-40 shrink-0 z-1!"><div class="sticky bg-token-bg-elevated-secondary"></div></div></div><div class="corner-superellipse/1.1 rounded-3xl bg-token-bg-elevated-secondary"><div class="relative z-0 flex max-w-full"><div id="code-block-viewer" dir="ltr" class="q9tKkq_viewer cm-editor z-10 light:cm-light dark:cm-light flex h-full w-full flex-col items-stretch ͼk ͼy"><div class="cm-scroller"><div class="cm-content q9tKkq_readonly"><span>Person(parent_id=root.id)</span></div></div></div></div></div></div></div></div><div class=""><div class=""></div></div></div></div></div></pre>

Add Grandchild:

<pre class="overflow-visible! px-0!" data-start="6284" data-end="6318"><div class="w-full my-4"><div class=""><div class="relative"><div class="h-full min-h-0 min-w-0"><div class="h-full min-h-0 min-w-0"><div class="border corner-superellipse/1.1 border-token-border-light bg-token-bg-elevated-secondary rounded-3xl"><div class="pointer-events-none absolute inset-x-4 top-12 bottom-4"><div class="pointer-events-none sticky z-40 shrink-0 z-1!"><div class="sticky bg-token-border-light"></div></div></div><div class="pointer-events-none absolute inset-x-px top-0 bottom-96"><div class="pointer-events-none sticky z-40 shrink-0 z-1!"><div class="sticky bg-token-bg-elevated-secondary"></div></div></div><div class="corner-superellipse/1.1 rounded-3xl bg-token-bg-elevated-secondary"><div class="relative z-0 flex max-w-full"><div id="code-block-viewer" dir="ltr" class="q9tKkq_viewer cm-editor z-10 light:cm-light dark:cm-light flex h-full w-full flex-col items-stretch ͼk ͼy"><div class="cm-scroller"><div class="cm-content q9tKkq_readonly"><span>Person(parent_id=child.id)</span></div></div></div></div></div></div></div></div><div class=""><div class=""></div></div></div></div></div></pre>

Hierarchy auto-forms.

---

# 17. Security Considerations

Always validate:

* User owns the family_tree
* Parent belongs to same tree
* Cannot modify another user’s tree

Authorization enforced at service layer.

---

# 18. Final Summary

The Family Tree system:

* Uses adjacency list modeling
* Supports recursive hierarchical data
* Is multi-tenant aware
* Is extendable for marriages and complex relationships
* Is scalable for medium-size genealogical datasets

The structure is flexible and production-ready for MVP.
