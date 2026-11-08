# AWS Architecture — AI System Design #1: FAQ Support Assistant

## 1. Recommended AWS architecture

Recommendation: Start with a serverless, deterministic FAQ service. Do not
introduce Amazon Bedrock or a vector database yet.

The completed design has a small approved FAQ repository, read-only answers,
source citations, and explicit abstention when evidence is missing. The AWS
architecture should preserve those properties.

I am assuming a public-facing e-commerce FAQ assistant, a small policy
collection, low-to-moderate traffic, and correctness as the highest priority.
The existing website remains outside the new backend.

```markdown
**Recommended starting stack**

**API entry** : `Amazon API Gateway — REST API`

**Compute**: `AWS Lambda (Python)`

**Source of truth**: `Amazon S3 with Versioning`

**API protection**: `AWS WAF`

**Monitoring**: `Amazon CloudWatch`

**Permissions**: `AWS IAM`

**Deployment**: `AWS SAM / CloudFormation`

**LLM / agent**: `Not required for V1`

```

Why this stack? AWS recommends API Gateway with Lambda for synchronous
serverless APIs. REST APIs support direct AWS WAF integration, while Lambda
avoids managing application servers.


For the small FAQ corpus, store one approved, versioned JSON policy bundle in S3
and read it from Lambda. S3 supports strongly consistent reads following
successful updates to a single object and retains previous versions when
Versioning is enabled.

This architecture is an AWS deployment proposal, not an already deployed system.

## 2. High-level AWS service comparison

| Concern                   | Recommended                        | Alternatives considered              | Decision                                                        |
|---------------------------|------------------------------------|--------------------------------------|-----------------------------------------------------------------|
| Public API                | API Gateway REST API               | HTTP API, ALB, Lambda Function URL   | REST chosen for direct WAF integration                          |
| Application compute       | Lambda                             | ECS Fargate, App Runner, EC2, EKS    | Lambda fits small request-driven code                           |
| Approved FAQ storage      | S3 Versioning                      | DynamoDB, Aurora                     | S3 is sufficient for a small read-only bundle                   |
| Search                    | Python matcher in Lambda           | OpenSearch, Bedrock Knowledge Bases  | Avoid a search service until needed                             |
| Text generation           | None initially                     | Amazon Bedrock models                | Exact approved answers are safer                                |
| API security              | AWS WAF                            | Custom Lambda filtering only         | Filter malicious or excessive traffic before backend processing |
| Identity                  | IAM roles for service/admin access | Cognito, IAM Identity Center         | No customer login required for public FAQs                      |
| Observability             | CloudWatch                         | External monitoring platforms        | Native AWS integration is sufficient                            |
| Infrastructure deployment | AWS SAM                            | CDK, Terraform, manual console setup | SAM is focused on serverless applications                       |

The rejected services are not poor choices generally. They are unnecessary for
the current requirements. If those requirements change, the recommendation may
also change.

## 3. AWS system integration diagram

This shows the recommended runtime, policy publishing, security, and monitoring
connections.

```
                    CUSTOMER REQUEST FLOW

+-----------------------------+
| Customer Website / Browser  |
+-----------------------------+
               |
               | HTTPS POST /faq/ask
               v
+-----------------------------+
| Amazon API Gateway REST API |
|                             |
| AWS WAF attached to stage   |
| - Traffic filtering         |
| - Rate-based protection     |
+-----------------------------+
               |
               | Lambda invocation
               v
+-----------------------------+
| AWS Lambda (Python)         |
|                             |
| 1. Validate input           |
| 2. Minimize sensitive data  |
| 3. Retrieve approved FAQs   |
| 4. Match question           |
| 5. Validate selected policy |
| 6. Answer or abstain        |
+-----------------------------+
               |
               | IAM-authorized GetObject
               v
+-----------------------------+
| Amazon S3                   |
| Private policy bucket       |
|                             |
| approved/current.json       |
|                             |
| Versioning enabled          |
| Business source of truth    |
+-----------------------------+

Lambda returns JSON to API Gateway,
which returns the response to the customer.


                    POLICY PUBLISHING

+-----------------------------+
| Authorized Policy Editor    |
+-----------------------------+
               |
               v
+-----------------------------+
| Review + Validation Pipeline|
| Tests + publication checks  |
+-----------------------------+
               |
               | Authorized publish
               v
+-----------------------------+
| S3 Approved Policy Bucket   |
| New object version          |
+-----------------------------+


                 CROSS-CUTTING CONTROLS

+-----------------------------+
| AWS IAM                     |
| Read-only Lambda role       |
| Separate publisher role     |
+-----------------------------+

+-----------------------------+
| Amazon CloudWatch           |
| Logs, metrics, alarms       |
| Latency, errors, abstention |
+-----------------------------+

+-----------------------------+
| AWS CloudTrail (optional)   |
| Audit policy object changes |
+-----------------------------+
```

The arrows describe the logical integrations. IAM provides permissions rather
than carrying customer traffic. CloudWatch receives telemetry from the API and
Lambda.

## 4. Why each service was selected

### A. API layer — Amazon API Gateway REST API

Recommended because the FAQ service is public-facing.

The REST API supports direct association with AWS WAF, request validation,
throttling controls, and Lambda integration. It gives us one managed entry point
rather than exposing backend compute directly.

| Alternative               | Why not selected                                                                   |
|---------------------------|------------------------------------------------------------------------------------|
| API Gateway HTTP API      | Lower-cost, simpler option, but lacks direct WAF stage integration                 |
| Lambda Function URL       | Very simple endpoint, but fewer API management features                            |
| Application Load Balancer | More suitable when routing to container services or multiple long-running backends |
| AppSync                   | GraphQL and subscription capabilities are unnecessary                              |

Trade-off: REST API is generally more expensive than HTTP API.

If the FAQ endpoint were accessible only to authenticated internal users, I
would choose HTTP API instead.

### B. Compute — AWS Lambda

The current Python implementation performs short, stateless operations:
validation, retrieval, matching, and response formatting.

Lambda is suitable because it executes application code per invocation without
requiring servers. AWS's compute guidance places Lambda in event-driven
workloads and Fargate in longer-running or persistent container workloads.

| Alternative      | When it becomes better                                                            |
|------------------|-----------------------------------------------------------------------------------|
| ECS with Fargate | Persistent service, custom runtime requirements, or sustained container workloads |
| AWS App Runner   | Existing containerized web application                                            |
| EC2              | Specific server or runtime control requirements                                   |
| EKS              | Organization already operates Kubernetes as its standard platform                 |

I would reject EKS and EC2 for this FAQ service because they add operational
responsibilities without improving the core matching problem.

### C. Storage — Amazon S3

Recommended: One versioned JSON bundle containing approved FAQ records.

A conceptual policy bundle:

```json
{
  "revision": "v2",
  "policies": [
    {
      "source_id": "FAQ-RETURN-01",
      "version": 2,
      "approved": true,
      "effective_from": "2026-01-01",
      "question": "Can I return an opened item?",
      "answer": "Opened items can be returned within 14 days if undamaged."
    }
  ]
}
```

S3 provides useful properties for this design: object version history and atomic
replacement of a single object. The application reads the latest approved bundle
rather than maintaining a separate search index.

| Alternative       | Why rejected for now                                                                           |
|-------------------|------------------------------------------------------------------------------------------------|
| DynamoDB          | Better for individual record access and frequent updates, but unnecessary for one small bundle |
| Aurora PostgreSQL | Relational database operations are unnecessary                                                 |
| OpenSearch        | Too much search infrastructure for a handful of curated FAQs                                   |

There is one important constraint: S3 Versioning is not policy approval. An
authorized publication process must validate the bundle before replacing the
current version. Also, S3's strong consistency applies to single-object updates;
it does not make updates across multiple objects atomic.

If the FAQ repository grows into thousands of frequently updated records,
DynamoDB becomes a stronger candidate. If complex full-text or semantic search
is required, use a dedicated search layer.

### D. Security, monitoring and deployment

| AWS service | Recommended use                                                                            |
|-------------|--------------------------------------------------------------------------------------------|
| AWS IAM     | Lambda can read only the approved policy object. A separate publishing role can modify it. |
| AWS WAF     | Apply managed rules and appropriate rate-based rules to the REST API stage.                |
| CloudWatch  | Record request outcomes, API errors, Lambda failures, latency and source-access failures.  |
| CloudTrail  | Audit sensitive policy object operations.                                                  |
| AWS SAM     | Define API Gateway, Lambda, IAM, S3 and monitoring resources as infrastructure code.       |

AWS SAM is an appropriate deployment choice for this serverless stack because it
provides simplified CloudFormation definitions and local development
support.

CloudTrail S3 object-level data events are not enabled by default. If detailed
policy publication auditing is required, configure the appropriate data-event
selectors explicitly.

Customer authentication through Cognito is unnecessary for answering public
FAQs. If later features expose order-specific information, authentication and
server-side per-customer authorization become mandatory.

## 5. How a customer request works

1. **Customer submits a question.**

   The website sends an HTTPS request to `POST /faq/ask`.

2. **AWS WAF and API Gateway handle the entry point.**

   WAF evaluates configured protections. API Gateway invokes Lambda.

3. **Lambda validates the request.**

   The question, locale, size, and input format are checked. Unnecessary
   sensitive information is rejected or minimized.

4. **Lambda reads the approved policy bundle from S3.**

   For V1, fetch the current object for each request to avoid an unbounded stale
   cache. Record the S3 version ID and validate effective policy dates.

5. **The matching logic finds relevant policy evidence.**

   A unique, sufficiently supported match returns the exact approved text.
   Missing, ambiguous, or unsupported evidence causes abstention.

6. **API Gateway returns the result.**

   The response contains the answer, status, and verified source ID.

### Failure behavior

| Failure                         | Expected behavior                                    |
|---------------------------------|------------------------------------------------------|
| Unsupported Black Friday policy | `insufficient_evidence`, empty source list           |
| S3 is unavailable               | HTTP 503; never invent an answer                     |
| Policy bundle is invalid        | HTTP 503; report an internal source problem          |
| New policy is published         | Subsequent reads use the new S3 version              |
| Excessive or malicious requests | WAF or API throttling rejects requests               |
| Lambda fails                    | Return an API error and record operational telemetry |

For concurrent requests during publication, some already-running requests may
have read the previous complete version. They must retain that version
identifier in their evidence record. If that is unacceptable, a stricter
publication and freshness protocol is required.

## 6. When to introduce Amazon Bedrock

Amazon Bedrock is **optional**, not required by the current architecture.

It becomes useful when the business wants natural-language explanations across
many varied policy documents, rather than returning known answers.

### Future RAG architecture

```
               KNOWLEDGE INGESTION

+---------------------------+
| Approved Policy Documents |
| Amazon S3                 |
+---------------------------+
              |
              v
+---------------------------+
| Amazon Bedrock            |
| Knowledge Bases           |
| Parsing + Embeddings      |
+---------------------------+
              |
              v
+---------------------------+
| Vector Storage            |
| S3 Vectors or OpenSearch  |
+---------------------------+


                 QUERY PATH

+---------------------------+
| Customer                  |
+---------------------------+
              |
              v
+---------------------------+
| API Gateway + Lambda      |
+---------------------------+
              |
              v
+---------------------------+
| Bedrock Knowledge Base    |
| Retrieve approved passages|
+---------------------------+
              |
              v
+---------------------------+
| Amazon Bedrock Model      |
| Generate answer draft     |
+---------------------------+
              |
              v
+---------------------------+
| Lambda Response Gate      |
| Verify source + claims    |
| Return or abstain         |
+---------------------------+
              |
              v
+---------------------------+
| Customer                  |
+---------------------------+
```

Amazon Bedrock Knowledge Bases supports S3 data sources and multiple vector
stores, including S3 Vectors and OpenSearch Serverless.

For that future design:

| Service                        | Recommendation                                                        | Reason                                                            |
|--------------------------------|-----------------------------------------------------------------------|-------------------------------------------------------------------|
| Amazon Bedrock Knowledge Bases | Conditional                                                           | Managed ingestion and retrieval when the corpus becomes complex   |
| Amazon S3 Vectors              | Evaluate first for simpler vector-search needs                        | Vector storage without requiring a general-purpose search cluster |
| Amazon OpenSearch Serverless   | Select when hybrid search and advanced search requirements justify it | Combines richer search capabilities with vector search            |
| Amazon Bedrock model           | Use only for needed synthesis                                         | Produces natural-language answers from retrieved evidence         |
| Bedrock Agents / AgentCore     | Reject for this FAQ case                                              | No autonomous multi-step tool orchestration is required           |

For example, if a customer asks about several related policy clauses, the RAG
pipeline can retrieve multiple passages and use a Bedrock model to prepare a
combined explanation.

The model output must still pass application-owned source and factual
validation. Neither RAG nor a managed foundation model guarantees correct
company policy answers.

## 7. Cost and operational trade-offs

Without expected request volume, region, payload size and latency target, a
credible monthly price estimate is not possible.

| Design                    | Relative complexity | Main cost drivers                                                       |
|---------------------------|---------------------|-------------------------------------------------------------------------|
| REST API + Lambda + S3    | Low                 | API requests, Lambda invocations/duration, S3 reads, WAF and monitoring |
| HTTP API + Lambda + S3    | Low                 | Generally lower API entry cost, but different protection options        |
| Lambda + DynamoDB         | Low–medium          | Requests, table storage, application logic                              |
| Bedrock + Knowledge Bases | Medium              | Model inference, embeddings, retrieval and vector storage               |
| ECS / EKS + OpenSearch    | Medium–high         | Running infrastructure, search capacity and operations                  |

A practical optimization order is to measure usage first, then optimize S3 reads
or move to an indexed store only when latency, cost, or retrieval requirements
justify it.

## 8. Final AWS service selection
```
**Deploy initially**

API Gateway REST API + AWS WAF + Lambda + versioned S3 + IAM + CloudWatch,
managed through AWS SAM.

**Add when required**

CloudTrail S3 data-event auditing, DynamoDB for richer FAQ records or feedback,
Cognito for authenticated features, and Bedrock Knowledge Bases for advanced
retrieval.

**Do not introduce yet**

EKS, ECS, OpenSearch, autonomous agents, Step Functions, MCP infrastructure, or
vector embeddings.
```

The central decision is to **keep approved policy storage, retrieval, and answer
authorization independent of an AI model**.

That preserves the most important property of AI Design #1: a missing policy
produces a safe abstention, not a fabricated answer.

