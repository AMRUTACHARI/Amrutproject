import React, { useEffect, useState, useMemo } from "react";
import { useSearchParams } from "react-router-dom";
import { Shell, PageHeader } from "@/components/Navbar";
import { ScanResult, statusColor } from "@/components/ScanResult";
import api, { apiError } from "@/lib/api";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import {
  Search,
  Trash2,
  Download,
  Eye,
  Loader2,
  Sprout,
  LayoutGrid,
  List,
  FileSpreadsheet,
  ArrowUpDown,
} from "lucide-react";
import { toast } from "sonner";

const STATUSES = ["All", "Healthy", "Leaf Spot", "Blight", "Root Rot", "Deficiency", "Pest Infestation", "Viral", "Wilt", "Unknown"];

export default function HistoryPage() {
  const [params] = useSearchParams();
  const [scans, setScans] = useState(null);
  const [query, setQuery] = useState("");
  const [status, setStatus] = useState("All");
  const [sortOrder, setSortOrder] = useState("newest");
  const [viewMode, setViewMode] = useState("grid");
  const [selected, setSelected] = useState(null);
  const [loadingDetail, setLoadingDetail] = useState(false);
  const [loadError, setLoadError] = useState("");

  const load = () =>
    api
      .get("/scans")
      .then((r) => { setScans(r.data.scans); setLoadError(""); })
      .catch((e) => { setScans([]); setLoadError(apiError(e)); });

  useEffect(() => {
    load();
  }, []);

  useEffect(() => {
    const id = params.get("scan");
    if (id) openScan(id);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [params]);

  const openScan = async (id) => {
    setLoadingDetail(true);
    try {
      const { data } = await api.get(`/scans/${id}`);
      setSelected(data.scan);
    } catch (e) {
      toast.error(apiError(e));
    } finally {
      setLoadingDetail(false);
    }
  };

  const remove = async (id) => {
    try {
      await api.delete(`/scans/${id}`);
      toast.success("Plant scan deleted.");
      setScans((s) => s.filter((x) => x.id !== id));
    } catch (e) {
      toast.error(apiError(e));
    }
  };

  const exportData = async () => {
    try {
      const { data } = await api.get("/users/me/export");
      const blob = new Blob([JSON.stringify(data, null, 2)], { type: "application/json" });
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = "floraai-plant-scans.json";
      a.click();
      URL.revokeObjectURL(url);
      toast.success("Plant scan history exported as JSON.");
    } catch (e) {
      toast.error(apiError(e));
    }
  };

  const exportCSV = () => {
    if (!scans || !scans.length) {
      toast.info("No plant scans available to export.");
      return;
    }
    const headers = ["ID", "Plant Name", "Scientific Name", "Family", "Status", "Health Score", "Confidence", "Date", "Diagnosis"];
    const rows = filtered.map((s) => [
      s.id || "",
      `"${(s.plant_name || "").replace(/"/g, '""')}"`,
      `"${(s.scientific_name || "").replace(/"/g, '""')}"`,
      `"${(s.plant_family || "").replace(/"/g, '""')}"`,
      s.status || "",
      s.health_score ?? "",
      s.confidence ?? "",
      new Date(s.created_at).toISOString().split("T")[0],
      `"${(s.diagnosis || "").replace(/"/g, '""')}"`,
    ]);
    const csvContent = [headers.join(","), ...rows.map((r) => r.join(","))].join("\n");
    const blob = new Blob([csvContent], { type: "text/csv;charset=utf-8;" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = "floraai-plant-records.csv";
    a.click();
    URL.revokeObjectURL(url);
    toast.success("Exported CSV spreadsheet.");
  };

  const filtered = useMemo(() => {
    if (!scans) return [];
    let list = scans.filter((s) => {
      const okStatus =
        status === "All"
          ? true
          : status === "NeedsAttention"
          ? s.status !== "Healthy"
          : s.status === status;
      const okQuery = !query || (s.plant_name || "").toLowerCase().includes(query.toLowerCase());
      return okStatus && okQuery;
    });

    if (sortOrder === "newest") {
      list.sort((a, b) => new Date(b.created_at) - new Date(a.created_at));
    } else if (sortOrder === "oldest") {
      list.sort((a, b) => new Date(a.created_at) - new Date(b.created_at));
    } else if (sortOrder === "health_asc") {
      list.sort((a, b) => (a.health_score ?? 0) - (b.health_score ?? 0));
    } else if (sortOrder === "health_desc") {
      list.sort((a, b) => (b.health_score ?? 0) - (a.health_score ?? 0));
    }
    return list;
  }, [scans, status, query, sortOrder]);

  const healthyCount = (scans || []).filter((scan) => scan.status === "Healthy").length;
  const attentionCount = (scans || []).filter((scan) => scan.status !== "Healthy").length;

  return (
    <Shell>
      <div className="mx-auto max-w-7xl px-4 py-8 sm:px-6 lg:px-8">
        <PageHeader
          eyebrow="My Plant History"
          title="Your scan history"
          description="Every saved plant check, with its photo, health result, and care report in one place."
          action={
            <div className="flex items-center gap-2">
              <Button
                variant="outline"
                size="sm"
                onClick={exportCSV}
                className="rounded-full border-primary/20 text-xs font-semibold uppercase tracking-wider hover:bg-secondary"
                title="Export as CSV spreadsheet"
              >
                <FileSpreadsheet className="mr-1.5 h-3.5 w-3.5" /> CSV
              </Button>
              <Button
                variant="outline"
                size="sm"
                onClick={exportData}
                className="rounded-full border-primary/20 text-xs font-semibold uppercase tracking-wider hover:bg-secondary"
                data-testid="export-data-button"
              >
                <Download className="mr-1.5 h-3.5 w-3.5" /> Export JSON
              </Button>
            </div>
          }
        />

        {/* Interactive Stats Cards */}
        <div className="mt-7 grid grid-cols-2 gap-3 lg:grid-cols-4">
          {[
            { label: "Saved scans", value: scans?.length ?? "—", filterValue: "All" },
            { label: "Healthy", value: scans ? healthyCount : "—", filterValue: "Healthy" },
            { label: "Needs attention", value: scans ? attentionCount : "—", filterValue: "NeedsAttention" },
            { label: "Showing", value: scans ? filtered.length : "—", filterValue: null },
          ].map((item) => (
            <div
              key={item.label}
              onClick={() => item.filterValue && setStatus(item.filterValue)}
              className={`rounded-2xl border px-4 py-3 shadow-xs transition-all ${
                item.filterValue
                  ? "cursor-pointer hover:border-primary/40 hover:bg-secondary/40"
                  : ""
              } ${status === item.filterValue ? "border-primary bg-primary/5" : "border-primary/10 bg-card"}`}
            >
              <p className="font-mono text-[10px] uppercase tracking-[0.16em] text-muted-foreground">{item.label}</p>
              <p className="mt-1 font-serif text-2xl font-semibold text-foreground">{item.value}</p>
            </div>
          ))}
        </div>

        {/* Search, Filter, Sort and Layout switch */}
        <div className="mt-8 flex flex-col gap-3 sm:flex-row items-stretch sm:items-center">
          <div className="relative flex-1">
            <Search className="absolute left-3.5 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
            <Input
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="Search your plants by name (e.g. Curry Leaf, Coconut, Mango, Rose)…"
              className="pl-10 rounded-xl"
              data-testid="history-search-input"
            />
          </div>

          <Select value={status} onValueChange={setStatus}>
            <SelectTrigger className="sm:w-52 rounded-xl" data-testid="history-status-filter">
              <SelectValue />
            </SelectTrigger>
            <SelectContent>
              {STATUSES.map((s) => (
                <SelectItem key={s} value={s}>
                  {s === "All" ? "All Health Statuses" : s}
                </SelectItem>
              ))}
              <SelectItem value="NeedsAttention">Needs Attention</SelectItem>
            </SelectContent>
          </Select>

          <Select value={sortOrder} onValueChange={setSortOrder}>
            <SelectTrigger className="sm:w-44 rounded-xl">
              <ArrowUpDown className="h-3.5 w-3.5 mr-1.5 text-muted-foreground" />
              <SelectValue placeholder="Sort by" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="newest">Newest First</SelectItem>
              <SelectItem value="oldest">Oldest First</SelectItem>
              <SelectItem value="health_desc">Highest Health</SelectItem>
              <SelectItem value="health_asc">Lowest Health</SelectItem>
            </SelectContent>
          </Select>

          <div className="hidden sm:flex items-center gap-1 border border-primary/20 rounded-xl p-1 bg-card">
            <button
              type="button"
              onClick={() => setViewMode("grid")}
              className={`p-1.5 rounded-lg transition-colors ${
                viewMode === "grid" ? "bg-primary text-primary-foreground" : "text-muted-foreground hover:text-foreground"
              }`}
              title="Grid view"
            >
              <LayoutGrid className="h-4 w-4" />
            </button>
            <button
              type="button"
              onClick={() => setViewMode("table")}
              className={`p-1.5 rounded-lg transition-colors ${
                viewMode === "table" ? "bg-primary text-primary-foreground" : "text-muted-foreground hover:text-foreground"
              }`}
              title="Compact list view"
            >
              <List className="h-4 w-4" />
            </button>
          </div>
        </div>

        {/* Results Section */}
        <div className="mt-8">
          {scans === null ? (
            <div className="flex justify-center py-20">
              <Loader2 className="h-6 w-6 animate-spin text-primary" />
            </div>
          ) : filtered.length === 0 ? (
            <Card className="rounded-3xl border-dashed border-primary/20 bg-transparent" data-testid="history-empty">
              <CardContent className="flex flex-col items-center gap-3 py-16 text-center">
                <Sprout className="h-10 w-10 text-muted-foreground/40" />
                <p className="text-sm text-muted-foreground max-w-md">
                  {loadError
                    ? `We couldn't load your scan history. ${loadError}`
                    : scans.length === 0
                    ? "No plants scanned yet. Take or upload your first photo on the Scan Plant page."
                    : "No saved scans match your search or filter."}
                </p>
              </CardContent>
            </Card>
          ) : viewMode === "table" ? (
            <div className="overflow-hidden rounded-2xl border border-primary/15 bg-card shadow-xs">
              <div className="overflow-x-auto">
                <table className="w-full text-left text-xs">
                  <thead className="bg-secondary/40 font-mono uppercase tracking-wider text-muted-foreground border-b border-primary/10">
                    <tr>
                      <th className="py-3 px-4">Plant</th>
                      <th className="py-3 px-4">Status</th>
                      <th className="py-3 px-4 text-center">Health</th>
                      <th className="py-3 px-4">Date</th>
                      <th className="py-3 px-4 text-right">Actions</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-primary/10">
                    {filtered.map((s) => (
                      <tr key={s.id} className="hover:bg-secondary/20 transition-colors">
                        <td className="py-3 px-4">
                          <div className="flex items-center gap-3">
                            {s.image_base64 ? (
                              <img src={s.image_base64} alt="" className="h-10 w-10 rounded-lg object-cover" />
                            ) : (
                              <div className="h-10 w-10 rounded-lg bg-secondary flex items-center justify-center">
                                <Sprout className="h-4 w-4 text-muted-foreground" />
                              </div>
                            )}
                            <div>
                              <p className="font-serif font-medium text-foreground text-sm">{s.plant_name || "Plant"}</p>
                              {s.scientific_name && <p className="font-serif italic text-muted-foreground text-[11px]">{s.scientific_name}</p>}
                            </div>
                          </div>
                        </td>
                        <td className="py-3 px-4">
                          <Badge className={`rounded-full border text-[10px] font-mono uppercase tracking-wider ${statusColor(s.status)}`}>
                            {s.status}
                          </Badge>
                        </td>
                        <td className="py-3 px-4 text-center font-mono font-bold text-foreground">
                          {s.health_score}/100
                        </td>
                        <td className="py-3 px-4 font-mono text-muted-foreground">
                          {new Date(s.created_at).toLocaleDateString()}
                        </td>
                        <td className="py-3 px-4 text-right">
                          <div className="flex items-center justify-end gap-1.5">
                            <Button size="sm" variant="ghost" onClick={() => openScan(s.id)} className="h-8 rounded-full px-2.5">
                              <Eye className="h-3.5 w-3.5 mr-1" /> View
                            </Button>
                            <Button size="sm" variant="ghost" onClick={() => remove(s.id)} className="h-8 w-8 p-0 text-destructive hover:bg-destructive/10">
                              <Trash2 className="h-3.5 w-3.5" />
                            </Button>
                          </div>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          ) : (
            <div className="grid gap-5 sm:grid-cols-2 lg:grid-cols-3" data-testid="history-grid">
              {filtered.map((s) => (
                <Card
                  key={s.id}
                  className="group overflow-hidden rounded-3xl border-primary/15 bg-card shadow-xs transition-all hover:-translate-y-1 hover:shadow-md hover:border-primary/30"
                  data-testid={`history-card-${s.id}`}
                >
                  <div className="relative h-44 overflow-hidden bg-secondary">
                    {s.image_base64 ? (
                      <img
                        src={s.image_base64}
                        alt={s.plant_name}
                        className="h-full w-full object-cover transition-transform duration-500 group-hover:scale-105"
                      />
                    ) : (
                      <div className="flex h-full w-full items-center justify-center bg-secondary/50 text-muted-foreground">
                        <Sprout className="h-8 w-8" />
                      </div>
                    )}
                    <Badge
                      className={`absolute left-3 top-3 rounded-full border backdrop-blur-md text-[10px] font-mono uppercase tracking-wider ${statusColor(
                        s.status
                      )}`}
                    >
                      {s.status}
                    </Badge>
                  </div>
                  <CardContent className="p-5">
                    <div className="flex items-start justify-between gap-2">
                      <div className="min-w-0">
                        <h4 className="truncate font-serif text-lg font-medium text-foreground group-hover:text-primary transition-colors">
                          {s.plant_name || "Plant"}
                        </h4>
                        {s.scientific_name && (
                          <p className="font-serif italic text-xs text-muted-foreground truncate">
                            {s.scientific_name}
                          </p>
                        )}
                        {s.plant_family && (
                          <span className="inline-block mt-1 font-mono text-[9px] uppercase tracking-wider text-primary bg-primary/10 px-2 py-0.5 rounded-full border border-primary/15">
                            {s.plant_family}
                          </span>
                        )}
                        <p className="font-mono text-[10px] text-muted-foreground mt-1">
                          {new Date(s.created_at).toLocaleDateString(undefined, {
                            month: "short",
                            day: "numeric",
                            year: "numeric",
                          })}
                        </p>
                      </div>
                      <div className="flex flex-col items-end">
                        <span className="font-mono text-xl font-bold text-foreground">
                          {s.health_score}
                        </span>
                        <span className="font-mono text-[8px] uppercase tracking-widest text-muted-foreground">
                          Health
                        </span>
                      </div>
                    </div>

                    <div className="mt-4 pt-3 border-t border-primary/10 flex gap-2">
                      <Button
                        size="sm"
                        variant="secondary"
                        className="flex-1 rounded-full text-xs font-semibold uppercase tracking-wider hover:bg-primary hover:text-primary-foreground transition-colors"
                        onClick={() => openScan(s.id)}
                        data-testid={`view-scan-${s.id}`}
                      >
                        <Eye className="mr-1.5 h-3.5 w-3.5" /> View Report
                      </Button>
                      <Button
                        size="sm"
                        variant="ghost"
                        className="rounded-full text-destructive hover:bg-destructive/10 hover:text-destructive h-8 w-8 p-0"
                        onClick={() => remove(s.id)}
                        data-testid={`delete-scan-${s.id}`}
                        title="Delete record"
                      >
                        <Trash2 className="h-3.5 w-3.5" />
                      </Button>
                    </div>
                  </CardContent>
                </Card>
              ))}
            </div>
          )}
        </div>
      </div>

      <Dialog open={!!selected || loadingDetail} onOpenChange={(o) => !o && setSelected(null)}>
        <DialogContent className="max-w-2xl rounded-3xl p-6" data-testid="scan-detail-dialog">
          <DialogHeader>
            <DialogTitle className="font-serif text-xl">Plant Health Report</DialogTitle>
          </DialogHeader>
          {loadingDetail ? (
            <div className="flex justify-center py-10">
              <Loader2 className="h-6 w-6 animate-spin text-primary" />
            </div>
          ) : (
            selected && <ScanResult scan={selected} />
          )}
        </DialogContent>
      </Dialog>
    </Shell>
  );
}
